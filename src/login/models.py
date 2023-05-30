from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.timezone import now

class T_Employee_Manager(BaseUserManager):
    """
    Custom model manager for user.
    """

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        :param email:
        :param password:
        :return:
        """

        # Create super user with username, email
        user = self.model(
            email=self.normalize_email(email),
        )
        # Set password
        user.set_password(password)
        # Save user object
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        :param email:
        :param password:
        :return:
        """
        # Create super user with username, email and password
        user = self.create_user(
            email,
            password=password,
        )
        # Set flag is_admin true
        user.is_admin = True
        # Save user object
        user.save(using=self._db)
        return user

    def get_queryset(self):
        """
        get all active user.
        :return: Queryset
        """
        return super(T_Employee_Manager, self).get_queryset().filter(
            is_active=True
        )


# Create your models here.
class t_Employee(AbstractBaseUser):
    """
    User model using Abstract Base user from django which provide basic
    entities by default.
    """

    # Constant fo max length for fields
    EMAIL_MAX_LENGTH = 254
    EMPLOYEE_NAME_MAX_LENGTH = 255
    WORK_COUNTRY_MAX_LENGTH = 50
    SBU_MAX_LENGTH = 10
    EMP_CODE_MAX_LENGTH = 10
    JOB_TITTLE_MAX_LENGTH = 100

    # Employee code of user
    employee_code = models.CharField(
        max_length=EMP_CODE_MAX_LENGTH, 
        primary_key=True,
        unique=True,
        blank=False,
        null=False, 
        verbose_name='EmployeeCode',
        db_column='EmployeeCode'
    )
  
    # EmployeeName for user
    employee_name = models.CharField(
        max_length=EMPLOYEE_NAME_MAX_LENGTH,
        verbose_name='EmployeeName',
        db_column='EmployeeName'
    )

    # Email id of user
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='EmailID',
        db_column='EmailID'
    )

    # Email id of user
    email_by_code = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
        default=None,
        verbose_name='EmailByCode',
        db_column='EmailByCode'
    )

    # Email id of user
    email_by_name = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
        default=None,
        verbose_name='EmailByName',
        db_column='EmailByName'
    )

    # Employee work country
    work_country = models.CharField(
        max_length=WORK_COUNTRY_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='WorkCountry',
        db_column='WorkCountry'
    )

    # SBU for employee
    sbu = models.CharField(
        max_length=SBU_MAX_LENGTH,
        blank=True,
        verbose_name='SBU',
        db_column='SBU'
    )

    # Owner details for employee
    owner = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Owner',
        blank=True,
        db_column='OwnerEmployeeCode'
    )

    owner_name = models.CharField(
        max_length=EMPLOYEE_NAME_MAX_LENGTH,
        blank=True,
        null=True,
        default=None,
        verbose_name='OwnerEmployeeName',
        db_column='OwnerEmployeeName'
    )

    owner_email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        blank=True,
        null=True,
        default=None,
        verbose_name='OwnerEmployeeEmailID',
        db_column='OwnerEmployeeEmailID'
    )

    # Employee job tittle
    job_title = models.CharField(
        max_length=JOB_TITTLE_MAX_LENGTH,
        blank=True,
        verbose_name='JobTitle',
        db_column='JobTitle'
    )

    # Create Date
    create_date_time = models.DateTimeField(
        default=now, 
        verbose_name='CreatedDate',
        db_column='CreatedDate'
    )

    # Exit date
    exit_date_time = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='ExitedDate',
        db_column='ExitedDate'
    )


    # Flag to check user is active or not
    is_active = models.BooleanField(
        default=True, 
        verbose_name='isActive',
        db_column='Status'
    )

    # Check user is admin or not
    is_admin = models.BooleanField(
        default=False, 
        verbose_name='isSuperUser',
        db_column='IsAdmin'
    )

    # Check user is owner or not
    is_owner = models.BooleanField(
        default=False, 
        verbose_name='IsOwner',
        db_column='IsOwner'
    )

    password = models.CharField(
        max_length=200,
        null=True, 
        blank=True,
    )

    objects = T_Employee_Manager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.employee_code

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        """
        Override save to check entity with object id is present or not
        :param args:
        :param kwargs:
        :return:
        """
        super(t_Employee, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "t_Employee"
        verbose_name_plural = "t_Employee"
