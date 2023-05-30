from rest_framework import serializers
from management.models import *


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = '__all__'


class EmployeeAuthDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAuthDC
        fields = '__all__'


class EmployeeAuthPCSerializer(serializers.ModelSerializer):
    pc_desc = serializers.SerializerMethodField()
    pc_code = serializers.SerializerMethodField()
    requester = serializers.ReadOnlyField(source='employee_code.employee_name')
    approver = serializers.ReadOnlyField(
        source='employee_code.owner.employee_name')

    def get_pc_desc(self, obj):
        if obj.profit_center:
            return obj.profit_center.profit_center_desc
        return ProfitCenter.objects.filter(profit_center_code=obj.profit_center_code).first().profit_center_desc

    def get_pc_code(self, obj):
        if obj.profit_center:
            return obj.profit_center.profit_center_code
        return obj.profit_center_code

    class Meta:
        model = EmployeeAuthPC
        fields = '__all__'
        read_only_fields = ('id',)
        extra_fields = ("pc_code", "pc_desc", "requester", "approver")


class EmployeeAuthSCSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAuthSC
        fields = '__all__'


class ProfitCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitCenter
        fields = '__all__'
        read_only_fields = ('id',)


class ProfitCenterDetailSerializer(serializers.ModelSerializer):
    mapping = EmployeeAuthPCSerializer(many=True)

    class Meta:
        model = ProfitCenter
        fields = '__all__'
        extra_fields = ['mapping']
        read_only_fields = ('id', 'mapping')


class ProfitCenterStagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitCenterStaging
        fields = '__all__'


class EmployeeRequestHistorySerializer(serializers.ModelSerializer):
    country_code = serializers.ReadOnlyField(source='country.country_code')
    pc_code = serializers.ReadOnlyField(
        source='profit_center.profit_center_code')
    pc_desc = serializers.ReadOnlyField(
        source='profit_center.profit_center_desc')
    requester_name = serializers.ReadOnlyField(
        source='requester.employee_name')
    approver_name = serializers.ReadOnlyField(source='approver.employee_name')

    class Meta:
        model = EmployeeRequestHistory
        fields = '__all__'
        read_only_fields = ('id',)
        extra_fields = ["country_code", "pc_code",
                        "pc_desc", "requester_name", "approver_name"]


class ProfitCenterStagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitCenterStaging
        fields = '__all__'
        read_only_fields = ('id',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
