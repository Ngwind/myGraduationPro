from django.contrib import admin
from django.db.models import ForeignKey
from django.contrib.admin import ModelAdmin
from users.models import Teacher, Student  # 忽略这些红色波浪线，其实是正确的
from .models import Course, Video, CourseProgress, Scores
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export.resources import ModelResource
from django.apps import apps
from django.db.models.query import QuerySet
import tablib
from collections import OrderedDict


# 视频观看进度
class ProgressResource(ModelResource):
    """视频观看进度导入导出文件配置"""
    def __init__(self):
        super(ProgressResource, self).__init__()
        # 获取所有字段的verbose_name并存放在字典
        field_list = apps.get_model('courses.CourseProgress')._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    class Meta:
        model = CourseProgress
        fields = ('video', 'student', 'progress')
        import_id_fields = ('video', 'student')
        export_order = fields
        skip_unchanged = True


@admin.register(CourseProgress)
class ProgressAdmin(ExportMixin, ModelAdmin):
    list_display = ('video', 'student', 'editdate', 'progress')
    search_fields = ('video__videoName', 'student__username')
    ordering = ('video', 'student')
    readonly_fields = ['video', 'student', 'progress']
    resource_class = ProgressResource

    def get_queryset(self, request):
        """函数作用：当前登录的普通用户只能看到自己课程的学生观看进度"""
        qs = super(ProgressAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(video__in=(Video.objects.filter(publisher=request.user)).values('id'))

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


# 课程
class CourseResource(ModelResource):
    """课程导入导出文件配置"""
    def __init__(self):
        super(CourseResource, self).__init__()
        # 获取所有字段的verbose_name并存放在字典
        field_list = apps.get_model('courses.Course')._meta.fields
        self.vname_dict = {}
        self.fkey = []
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name
            if isinstance(i, ForeignKey):
                self.fkey.append(i.name)

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        dicts = []
        l_id = Course.objects.latest('id').id + 1
        for row in dataset.dict:
            tmp = OrderedDict()
            tmp['ID'] = l_id
            for item in row:
                if item == self.vname_dict['publisher']:
                    tmp[item] = Teacher.objects.get(username=row[self.vname_dict['publisher']]).id
                else:
                    tmp[item] = row[item]
            l_id = l_id + 1
            dicts.append(tmp)
        dataset.dict = dicts

    def export(self, queryset=None, *args, **kwargs):
        self.before_export(queryset, *args, **kwargs)
        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)
        # --------------------- #
        # 获取所有外键名称在headers中的位置
        fk_index = {}
        for fk in self.fkey:
            fk_index[fk] = headers.index(self.vname_dict[fk])
        # --------------------- #
        if isinstance(queryset, QuerySet):
            iterable = queryset.iterator()
        else:
            iterable = queryset
        for obj in iterable:
            """改写数据集"""
            # --------------------- #
            res = self.export_resource(obj)
            res[fk_index['publisher']] = Teacher.objects.get(id=res[fk_index['publisher']]).username
            data.append(res)
            # --------------------- #
        self.after_export(queryset, data, *args, **kwargs)
        return data

    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    class Meta:
        model = Course
        fields = ('courseName', 'publisher', 'publisher__first_name')
        import_id_fields = ('courseName', 'publisher')
        export_order = fields
        skip_unchanged = True


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ('courseName', 'publisher', 'createdate')
    resource_class = CourseResource

    def get_queryset(self, request):
        """函数作用：使当前登录的普通用户只能看到自己负责的课程"""
        qs = super(CourseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(publisher=request.user)


# 视频
class VideoResource(ModelResource):
    """视频导入导出文件配置"""
    def __init__(self):
        super(VideoResource, self).__init__()
        # 获取所有字段的verbose_name并存放在字典
        field_list = apps.get_model('courses.Video')._meta.fields
        self.vname_dict = {}
        self.fkey = []
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name
            if isinstance(i, ForeignKey):
                self.fkey.append(i.name)

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        dicts = []
        l_id = Video.objects.latest('id').id + 1
        for row in dataset.dict:
            tmp = OrderedDict()
            tmp['ID'] = l_id
            for item in row:
                if item == self.vname_dict['publisher']:
                    tmp[item] = Teacher.objects.get(username=row[self.vname_dict['publisher']]).id
                elif item == self.vname_dict['course']:
                    tmp[item] = Course.objects.get(courseName=row[self.vname_dict['course']]).id
                else:
                    tmp[item] = row[item]
            l_id = l_id + 1
            dicts.append(tmp)
        dataset.dict = dicts

    def export(self, queryset=None, *args, **kwargs):
        self.before_export(queryset, *args, **kwargs)
        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)
        # --------------------- #
        # 获取所有外键名称在headers中的位置
        fk_index = {}
        for fk in self.fkey:
            fk_index[fk] = headers.index(self.vname_dict[fk])
        # --------------------- #
        if isinstance(queryset, QuerySet):
            iterable = queryset.iterator()
        else:
            iterable = queryset
        for obj in iterable:
            """改写数据集"""
            # --------------------- #
            res = self.export_resource(obj)
            res[fk_index['publisher']] = Teacher.objects.get(id=res[fk_index['publisher']]).username
            res[fk_index['course']] = Course.objects.get(id=res[fk_index['course']]).courseName
            data.append(res)
            # --------------------- #
        self.after_export(queryset, data, *args, **kwargs)
        return data

    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    class Meta:
        model = Video
        fields = ('chapterId', 'videoName', 'videoUrl', 'publisher', 'course',)
        import_id_fields = ('videoName', 'course', 'publisher',)
        export_order = fields
        skip_unchanged = True


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    list_display = ('videoName', 'chapterId', 'videoUrl', 'course', 'publisher', 'createdate', 'editdate')
    search_fields = ['videoName', 'publisher__first_name', 'course__courseName']
    # list_filter = ['publisher', 'course']
    ordering = ['publisher', 'course', 'chapterId']
    resource_class = VideoResource

    def get_queryset(self, request):
        """函数作用：使当前登录的普通用户只能看到自己添加的课程"""
        qs = super(VideoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(publisher=request.user)


# 成绩
class ScoresResource(ModelResource):
    """成绩导入导出文件配置"""
    def __init__(self):
        super(ScoresResource, self).__init__()
        # 获取所有字段的verbose_name并存放在字典
        field_list = apps.get_model('courses.Scores')._meta.fields
        self.vname_dict = {}
        self.fkey = []
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name
            if isinstance(i, ForeignKey):
                self.fkey.append(i.name)

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        dicts = []
        l_id = Scores.objects.latest('id').id + 1
        for row in dataset.dict:
            tmp = OrderedDict()
            tmp['ID'] = l_id
            for item in row:
                if item == self.vname_dict['course']:
                    tmp[item] = Course.objects.get(courseName=row[self.vname_dict['course']]).id
                elif item == self.vname_dict['student']:
                    tmp[item] = Student.objects.get(studentId=row[self.vname_dict['student']]).studentId
                else:
                    tmp[item] = row[item]
            l_id = l_id + 1
            dicts.append(tmp)
        dataset.dict = dicts

    def export(self, queryset=None, *args, **kwargs):
        self.before_export(queryset, *args, **kwargs)
        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)
        # --------------------- #
        # 获取所有外键名称在headers中的位置
        fk_index = {}
        for fk in self.fkey:
            fk_index[fk] = headers.index(self.vname_dict[fk])
        # --------------------- #
        if isinstance(queryset, QuerySet):
            iterable = queryset.iterator()
        else:
            iterable = queryset
        for obj in iterable:
            """改写数据集"""
            # --------------------- #
            res = self.export_resource(obj)
            res[fk_index['course']] = Course.objects.get(id=res[fk_index['course']]).courseName
            res[fk_index['student']] = Student.objects.get(studentId=res[fk_index['student']]).studentId
            data.append(res)
            # --------------------- #
        self.after_export(queryset, data, *args, **kwargs)
        return data

    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
                pass
        return fields

    class Meta:
        model = Scores
        fields = ('course', 'student', 'score', 'student__username', 'student__userclass', 'student__college')
        import_id_fields = ('course', 'student',)
        export_order = fields
        skip_unchanged = True


@admin.register(Scores)
class ScoresAdmin(ImportExportModelAdmin):
    list_display = ('course', 'student', 'score')
    search_fields = ['student__username', 'course__courseName']
    ordering = ['course', 'score']
    readonly_fields = ['course', 'student']
    resource_class = ScoresResource

    def get_queryset(self, request):
        """函数作用：当前登录的普通用户只能看到自己课程的成绩"""
        qs = super(ScoresAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__in=(Course.objects.filter(publisher=request.user)).values('id'))

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


admin.site.site_header = 'GDUT在线教学管理系统'
admin.site.site_title = '教务管理'
