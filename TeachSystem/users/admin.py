from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export import resources
from django.apps import apps
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import Teacher, Student
from courses.models import CourseProgress, Video  # 忽略这些红色波浪线，其实是正确的


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
    readonly_fields = ['studentId', 'username', 'college', 'userclass', 'createdate', 'password', 'gender']
    # list_editable = ['college', 'userclass']
    resource_class = StudentResource

    # def get_queryset(self, request):
    #     """限定普通用户只能看到自己学生的信息"""
    #     qs = super(StudentAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(studentId__in=(CourseProgress.objects.filter(video__in=Video.objects.filter(publisher=request.user).values('id'))).values('student'))

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
