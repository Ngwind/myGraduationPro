from collections import OrderedDict
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export import resources
from django.apps import apps
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import Teacher, Student, Openid, Feedback
from courses.models import CourseProgress, Video, Scores, Course  # 忽略这些红色波浪线，其实是正确的


def _make_action(course, course_obj):
    """动态创建StudentAdmin的action"""
    def binding_to_video(StudentAdmin, request, queryset):
        """创建指定课程的Scores的action函数"""
        for stu in queryset:
            res = Scores.objects.update_or_create(defaults={'score': 0}, course=course_obj, student=stu)  # course课程主键, student学生主键
        messages.success(request, '操作成功！')
        pass
    binding_to_video.func_name = 'binding_to_video_{}'.format(course_obj.id)
    binding_to_video.short_description = '添加所选学生到课程:{}'.format(course)
    return binding_to_video


# ---------------学生------------------
class StudentResource(resources.ModelResource):
    """学生导入导出文件配置"""

    def __init__(self):
        super(StudentResource, self).__init__()
        # 获取所有字段的verbose_name并存放在字典
        field_list = apps.get_model('users.Student')._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        """默认导入导出field的column_name为字段的名称，这里修改为字段的verbose_name"""
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    class Meta:
        model = Student
        fields = ('studentId', 'username', 'college', 'userclass', 'password', )
        import_id_fields = ('studentId',)
        export_order = ('studentId', 'username', 'college', 'userclass', 'password', )
        skip_unchanged = True


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    """学生admin后台配置"""
    list_display = ('studentId', 'username', 'college', 'userclass')
    search_fields = ['studentId', 'username', 'college', 'userclass']
    list_filter = ['college', ]
    ordering = ('college', 'userclass', 'studentId')
    readonly_fields = ['studentId', 'username', 'college', 'userclass', 'password', 'gender']
    # list_editable = ['college', 'userclass']
    resource_class = StudentResource
    # actions = [_make_action(course, course_id) for course, course_id in ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        qs = Course.objects.filter(publisher=request.user.id)
        for obj in qs:
            func = _make_action(obj.courseName, obj)
            name = func.func_name
            desc = func.short_description
            actions[name] = (func, name, desc)
        return OrderedDict(actions)

    def get_readonly_fields(self, request, obj=None):
        """设置普通用户不能编辑学生信息"""
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


# ---------------教师------------------
class TeacherResource(resources.ModelResource):
    """教师导入导出文件配置"""
    def __init__(self):
        super(TeacherResource, self).__init__()
        # 获取所有字段的verbose_name并存放在字典
        field_list = apps.get_model('users.Teacher')._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def after_save_instance(self, instance, using_transactions, dry_run):
        """在导入teacher后，添加到特定组里"""
        if not dry_run:
            instance.groups.add(Group.objects.get(name='任课教师'))

    def get_export_fields(self):
        """默认导入导出field的column_name为字段的名称，这里修改为字段的verbose_name"""
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    class Meta:
        model = Teacher
        fields = ('username', 'first_name', 'college','is_staff')
        import_id_fields = ('username',)
        export_order = ('username', 'first_name', 'college', 'is_staff')
        skip_unchanged = True


@admin.register(Teacher)
class TeacherAdmin(ImportExportMixin, UserAdmin):
    """教师admin配置"""
    list_display = ['id', 'username', 'first_name', 'college', 'is_staff', 'date_joined', 'password']
    ordering = ['id', ]
    list_display_links = ['username', ]
    resource_class = TeacherResource
    actions = ["set_init_password"]
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('college', )}), ) + UserAdmin.add_fieldsets
    fieldsets = ((None, {'fields': ('college', )}), ) + UserAdmin.fieldsets
    list_filter = ('college', 'groups', 'is_superuser', 'is_active',)

    def set_init_password(self, request, queryset):
        """初始化密码action函数"""
        init_password = 'gdut123456'
        init_password_sercet = make_password(init_password)
        update_row = queryset.update(password=init_password_sercet)
        self.message_user(request, str(update_row)+"个用户密码成功初始化为"+init_password, fail_silently=False)
    set_init_password.short_description = "将选中用户密码初始化"


# ---------------openid------------------
@admin.register(Openid)
class OpenidAdmin(ModelAdmin):
    list_display = ['pk', 'openid', 'studentid', 'createdate', 'editdate']
    # search_fields = ['studentid']


# ---------------feedfack-----------------
@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    list_display = ['openid', 'createdate']
    readonly_fields = ['openid', 'createdate', 'context']
