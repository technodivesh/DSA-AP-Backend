
from __future__ import unicode_literals
from email.policy import default
# from http import client
# import uuid
from django.db import models
# Datetime imports
from django.utils.timezone import get_current_timezone, now
from datetime import date, datetime
import datetime as dt
from login.models import t_Employee
from django.db.models.signals import pre_save, post_save

MAX_LENGTH_GENERAL = 1000
PROFIT_CENTER_CODE_MAX_LENGTH = 10
COMPANY_CODE_MAX_LENGTH = 4
CLIENT_CODE_MAX_LENGTH = 50
PROFIT_CENTER_DESC_MAX_LENGTH = 50
CHAR_FIELD_MAX_LENGTH = 50
EMP_CODE_MAX_LENGTH = 50
DC_CODE_MAX_LENGTH = 50
CUSTOMER_GROUP_CODE_MAX_LENGTH = 50
COUNTRY_NAME_MAX_LENGTH = 50
COUNTRY_CODE_MAX_LENGTH = 2
COUNTRY_GENERAL_LENGTH = 30
SALES_CODE_MAX_LENGTH = 50
# Create your models here.


class CustomerGroup(models.Model):
    """
    Customer group model
    """

    id = models.AutoField(
        primary_key=True,
        verbose_name='CustomerGroupId',
        db_column='CustomerGroupId'
    )
    employee_code = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='EmployeeCode',
        db_column='EmployeeCode'
    )
    customer_group_code = models.CharField(max_length=EMP_CODE_MAX_LENGTH, blank=True, verbose_name='CustomerGroupCode',db_column='CustomerGroupCode')
    start_date = models.DateTimeField(default=now, verbose_name='StartDate',db_column='StartDate')
    end_date = models.DateTimeField(default=None,null=True, blank=True, verbose_name='EndDate',db_column='EndDate')
    status = models.BooleanField(default=True, verbose_name='Status',db_column='isActive')

    def __str__(self):
        return str(self.customer_group_id)

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        super(CustomerGroup, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_CustomerGroup"
        verbose_name_plural = "t_CustomerGroup"

class Country(models.Model):
    """
    Country table
    """


    # country_id= models.UUIDField( default=uuid.uuid4, verbose_name='CountryID')
    id = models.AutoField(
        primary_key=True,
        verbose_name='CountryID',
        db_column='CountryID'
    )
    client = models.IntegerField(null=False,db_column='Client')
    country_code = models.CharField(
        max_length=COUNTRY_CODE_MAX_LENGTH,
        db_column='CountryCode',
        # primary_key=True,
        unique=True,
        blank=False,
        null=False, 
    )
    country_name = models.CharField(max_length=COUNTRY_NAME_MAX_LENGTH,db_column='CountryName')
    region = models.CharField(blank=True , max_length=COUNTRY_GENERAL_LENGTH,db_column='Region')
    geography = models.CharField(blank=True , max_length=COUNTRY_GENERAL_LENGTH,db_column='Geography')
    region_value = models.CharField(blank=True , max_length=COUNTRY_GENERAL_LENGTH,db_column='Region_Value')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='CreatedDateTime',db_column='CreatedDateTime')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='UpdatedDateTime',db_column='UpdatedDateTime')
    region_volme = models.CharField(blank=True , max_length=COUNTRY_GENERAL_LENGTH,db_column='Region_VolME')


    def __str__(self):
        return f"{self.country_code}"

    def __unicode__(self):
        return f"{self.country_code}"

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        # self.updated_date = datetime.now().replace(tzinfo=get_current_timezone())
        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_Country"
        verbose_name_plural = "t_Country"
        unique_together = ('client', 'country_code')


class EmployeeAuthDC(models.Model):
    """
    Employee auth DC model
    """



    # employee_auth_id = models.UUIDField( default=uuid.uuid4, verbose_name='EmployeeAuthID')
    id = models.AutoField(
        primary_key=True,
        verbose_name='EmployeeAuthID',
        db_column='EmployeeAuthID'
    )
    employee_code = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='EmployeeCode',
        db_column='EmployeeCode'

    )
    client = models.CharField(
        max_length=CLIENT_CODE_MAX_LENGTH, 
        blank=True, 
        verbose_name='Client',
        db_column='Client'
    )
    dc_code = models.CharField(
        max_length=DC_CODE_MAX_LENGTH, 
        blank=True, 
        verbose_name='DCCode',
        db_column='DCCode'
    )
    company_code = models.CharField(
        max_length=COMPANY_CODE_MAX_LENGTH, 
        blank=True, 
        verbose_name='CompanyCode',
        db_column='CompanyCode'
    )
    start_date = models.DateTimeField(
        default=now, 
        verbose_name='StartDate',
        db_column='StartDate'
    )
    end_date = models.DateTimeField(
        default=None,
        null=True, 
        blank=True,
        verbose_name='EndDate',
        db_column='EndDate'
    )
    status = models.BooleanField(
        default=True, 
        verbose_name='Status',
        db_column='isActive'
        )

    def __str__(self):
        return str(self.dc_code)

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        super(EmployeeAuthDC, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_EmployeeAuthDC"
        verbose_name_plural = "t_EmployeeAuthDC"


class ProfitCenter(models.Model):
    """
    Profit center  model
    """

    id = models.AutoField(
        primary_key=True,
        verbose_name='ProfitCenterID',
        db_column='ProfitCenterID'
    )
    client = models.IntegerField(
        verbose_name='Client',
        db_column='Client'
    )
    profit_center_code = models.CharField(
        max_length=PROFIT_CENTER_CODE_MAX_LENGTH,
        verbose_name='ProfitCenterCode',
        db_column='ProfitCenterCode'
    )
    profit_center_desc = models.CharField(
        max_length=PROFIT_CENTER_DESC_MAX_LENGTH, 
        blank=True,
        verbose_name='ProfitCenterDesc',
        db_column='ProfitCenterDesc'
    )
    company_code = models.CharField(
        max_length=COMPANY_CODE_MAX_LENGTH, 
        verbose_name='CompanyCode',
        db_column='CompanyCode'
    )
    business_line = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        null=True,
        blank=True,
        verbose_name='BusinessLine',
        db_column='BusinessLine'
    )
    business_geography = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='BusinessGeography',
        db_column='BusinessGeography'
    )
    business_segment = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='BusinessSegment',
        db_column='BusinessSegment'
    )
    mis_business_vertical = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True,
        null=True,
        verbose_name='MISBusinessVertical',
        db_column='MISBusinessVertical'
    )
    mis_business_unit = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True,
        null=True, 
        verbose_name='MISBusinessUnit',
        db_column='MISBusinessUnit'
    )
    business_brand = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True,
        null=True, 
        verbose_name='BusinessBrand',
        db_column='BusinessBrand'
    )
    product_group = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='ProductGroup',
        db_column='ProductGroup'
    )
    flash_pg = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='FlashPG',
        db_column='FlashPG'
    )
    me_tel_pg = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True,
        null=True, 
        verbose_name='MeTelPG',
        db_column='MeTelPG'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Status',
        db_column='Status'
        )
    created_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='CreatedDateTime',
        db_column='CreatedDateTime'
    )
    updated_date = models.DateTimeField(
        auto_now=True, 
        verbose_name='UpdatedDateTime',
        db_column='UpdatedDateTime'
    )
    business_unit = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        verbose_name='BusinessUnit',
        db_column='BusinessUnit'
    )
    sbu = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        verbose_name='SBU',
        db_column='SBU'
    )


    def __str__(self):
        return f"{self.profit_center_code}"

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        # self.updated_date = datetime.now().replace(tzinfo=get_current_timezone())
        super(ProfitCenter, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_ProfitCenter"
        verbose_name_plural = "t_ProfitCenter"
        unique_together = ('client', 'profit_center_code','company_code')
        ordering = ['id']


class ProfitCenterStaging(models.Model):
    """
    Profit center staging model
    """
    # id = models.AutoField(
    #     primary_key=True,
    #     verbose_name='ProfitCenterID',
    #     # db_column='ProfitCenterID'
    # )
    client = models.IntegerField(
        verbose_name='Client',
        db_column='Client',
        default=300
    )
    profit_center_code = models.CharField(
        max_length=PROFIT_CENTER_CODE_MAX_LENGTH,
        verbose_name='ProfitCenterCode',
        db_column='ProfitCenterCode'
    )
    profit_center_desc = models.CharField(
        max_length=PROFIT_CENTER_DESC_MAX_LENGTH, 
        verbose_name='ProfitCenterDesc',
        db_column='ProfitCenterDesc'
    )
    company_code = models.CharField(
        max_length=COMPANY_CODE_MAX_LENGTH, 
        verbose_name='CompanyCode',
        db_column='CompanyCode'
    )
    business_line = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        null=True,
        blank=True,
        verbose_name='BusinessLine',
        db_column='BusinessLine'
    )
    business_geography = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='BusinessGeography',
        db_column='BusinessGeography'
    )
    business_segment = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='BusinessSegment',
        db_column='BusinessSegment'
    )
    mis_business_vertical = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True,
        null=True,
        verbose_name='MISBusinessVertical',
        db_column='MISBusinessVertical'
    )
    mis_business_unit = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='MISBusinessUnit',
        db_column='MISBusinessUnit'
    )
    business_brand = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='BusinessBrand',
        db_column='BusinessBrand'
    )
    product_group = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True,
        null=True, 
        verbose_name='ProductGroup',
        db_column='ProductGroup'
    )
    flash_pg = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True,
        null=True, 
        verbose_name='FlashPG',
        db_column='FlashPG'
    )
    me_tel_pg = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        null=True,
        verbose_name='MeTelPG',
        db_column='MeTelPG'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Status',
        db_column='Status'
        )
    created_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='CreatedDateTime',
        db_column='CreatedDateTime'
    )
    updated_date = models.DateTimeField(
        auto_now=True, 
        verbose_name='UpdatedDateTime',
        db_column='UpdatedDateTime'
    )
    business_unit = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        verbose_name='BusinessUnit',
        db_column='BusinessUnit'
    )
    sbu = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH, 
        blank=True, 
        verbose_name='SBU',
        db_column='SBU'
    )
    requester = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requester',
        db_column='requester'
    )
    state = models.CharField(default="New",blank=False,max_length=10,db_column='state')
    comments = models.CharField(blank=True,max_length=250)
    approver = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approver',
        db_column='approver'
    )

    def __str__(self):
        return f"{self.profit_center_code}"

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        self.client = 300
        super(ProfitCenterStaging, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_ProfitCenterStaging"
        verbose_name_plural = "t_ProfitCenterStaging"


class EmployeeAuthPC(models.Model):
    """
    Employee auth pc model
    """

    id = models.AutoField(
        primary_key=True,
        verbose_name='EmployeeAuthID',
        db_column='EmployeeAuthID'
    )
    country =  models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='country',
        related_name='country',
        db_column='fk_country'
    )
    country_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        verbose_name='CountryCode',
        db_column='CountryCode'
    )
    employee_code = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='EmployeeCode',
        db_column='EmployeeCode'
    )
    profit_center = models.ForeignKey(
        ProfitCenter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='profit_center',
        related_name='mapping',
        db_column='fk_profit_center'
    )
    profit_center_code = models.CharField(
        max_length=PROFIT_CENTER_CODE_MAX_LENGTH,
        null=True,
        blank=True,
        verbose_name='ProfitCenterCode',
        db_column='ProfitCenterCode'
    )
    start_date = models.DateTimeField(
        default = now,
        verbose_name='StartDate',
        db_column='StartDate'
    )
    end_date = models.DateTimeField(
        default=None,
        null=True, 
        blank=True,
        verbose_name='EndDate',
        db_column='EndDate'
    )
    status = models.BooleanField(
        default=True, 
        verbose_name='Status',
        db_column='Status'
    )
    customer_group_id = models.ForeignKey(
        CustomerGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='CustomerGroupID',
        db_column='CustomerGroupID'
    )

    def __str__(self):
        return f"{self.employee_code}-{self.profit_center_code}-{self.country_code}"

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        super(EmployeeAuthPC, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_EmployeeAuthPC"
        verbose_name_plural = "t_EmployeeAuthPC"
        # ordering = ['employee_auth_id']

def EmployeeAuthPC_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.country_code = instance.country.country_code
        instance.profit_center_code = instance.profit_center.profit_center_code
        instance.save()

post_save.connect(EmployeeAuthPC_post_save, sender=EmployeeAuthPC)


class EmployeeAuthSC(models.Model):
    """
    Employee auth sc model
    """

    id = models.AutoField(
        primary_key=True,
        verbose_name='EmployeeAuthID',
        db_column='EmployeeAuthID'
    )
    employee_code = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='EmployeeCode',
        db_column='EmployeeCode'
    )
    sales_code = models.CharField(
        max_length=SALES_CODE_MAX_LENGTH, 
        blank=True, 
        verbose_name='SalesCode',
        db_column='SalesCode'
    )
    start_date = models.DateTimeField(
        default = now,
        verbose_name='StartDate',
        db_column='StartDate'
    )
    end_date = models.DateTimeField(
        default=None,
        null=True, 
        blank=True, 
        verbose_name='EndDate',
        db_column='EndDate'
    )
    status = models.BooleanField(
        default=True, 
        verbose_name='Status',
        db_column='isActive'
    )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        super(EmployeeAuthSC, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_EmployeeAuthSC"
        verbose_name_plural = "t_EmployeeAuthSC"


class EmployeeRequestHistory(models.Model):
    """
    Employee request history
    """
    requester = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        # blank=True,
        verbose_name='RequesterID',
        related_name='RequesterID'
    )
    status = models.CharField(default="New",blank=False,max_length=10)
    profit_center = models.ForeignKey(
        ProfitCenter,
        on_delete=models.SET_NULL,
        null=True,
        # blank=True,
        verbose_name='ProfitCenterID',
    )
    approver = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ApproverID',
        related_name='ApproverID'
    )
    comments = models.CharField(blank=True,max_length=MAX_LENGTH_GENERAL)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        # blank=True,
        verbose_name='CountryID',
        related_name='countryID'
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='CreatedDateTime')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='UpdatedDateTime')
    start_date = models.DateTimeField(default = now, verbose_name='StartDate')
    end_date = models.DateTimeField(default = None, null=True, blank=True, verbose_name='EndDate')
    created_by = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='createrID',
        related_name='createrID',
        db_column='created_by'
    )
    updated_by = models.ForeignKey(
        t_Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='UpdaterID',
        related_name='UpdaterID',
        db_column='updated_by'
    )

    def __str__(self):
        return f"{self.id}-{self.requester}-{self.profit_center}"

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        super(EmployeeRequestHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_EmployeeRequestHistory"
        verbose_name_plural = "t_EmployeeRequestHistory"
        ordering = ['-id']
    

















