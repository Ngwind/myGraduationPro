from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export import resources
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Student
from courses.models import CourseProgress, Video  # 忽略这些红色波浪线，其实是正确的


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
    list_display = ('studentId', 'username', 'college', 'userclass', 'createdate')
    search_fields = ['studentId', 'username', 'college', 'userclass']
    list_filter = ['college', 'userclass']
    ordering = ('college', 'userclass', 'studentId')
    readonly_fields = ['studentId', 'username', 'college', 'userclass', 'createdate', 'password', 'gender']
    # list_editable = ['college', 'userclass']
    resource_class = StudentResource

    def get_queryset(self, request):
        """限定普通用户只能看到自己学生的信息"""
        qs = super(StudentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(studentId__in=(CourseProgress.objects.filter(video__in=Video.objects.filter(publisher=request.user).values('id'))).values('student'))

    def get_readonly_fields(self, request, obj=None):
        """设置普通用户不能编辑学生信息"""
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class TeacherResource(resources.ModelResource):
    """教师导入导出文件配置"""
    def __init__(self):
        super(TeacherResource, self).__init__()
        # 获取所有字段的verbose_name并存放在字典
        field_list = apps.get_model('users.Teacher')._meta.fields
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
        model = Teacher
        fields = ('username', 'first_name', 'college',)
        # import_id_fields = ('id',)
        export_order = ('username', 'first_name', 'college',)
        skip_unchanged = True



@admin.register(Teacher)
class TeacherAdmin(ImportExportMixin, UserAdmin):
    """教师admin配置"""
    list_display = ['first_name', 'username', 'college', 'is_staff', 'date_joined']
    ordering = ['first_name', 'username', 'college', 'is_staff', 'date_joined']
    resource_class = TeacherResource

    def get_fieldsets(self, request, obj=None):
        """在教师信息界面中的'个人信息'中添加college字段"""
        tp = super(UserAdmin, self).get_fieldsets(request, obj)
        ls = list(tp)
        new_list = list(ls[1][1]['fields'])
        if 'college' not in new_list:
            new_list.append('college')
        new_tp = tuple(new_list)
        ls[1][1]['fields'] = new_tp
        return tuple(ls)
