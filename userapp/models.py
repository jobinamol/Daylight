from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator
from django.utils import timezone
from adminpanal.models import PackageManagement
from staffs.models import Room
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.timezone import now



# User Model
class UserDBManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)

class UserDB(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # or UUIDField

    name = models.CharField(max_length=255)
    mobilenumber = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message='Mobile number must be between 10 and 15 digits and can optionally start with a "+" sign.'
            )
        ]
    )
    emailid = models.EmailField(unique=True)  # Ensure unique email
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    age = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999)
        ]
    )
    sex = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ]
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$', 
                message='Username may only contain letters, numbers, and @/./+/-/_ characters.'
            )
        ]
    )
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    last_login = models.DateTimeField(default=timezone.now)  # Add last_login field
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='userdb_set',
        related_query_name='userdb'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='userdb_set',
        related_query_name='userdb'
    )

    objects = UserDBManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'emailid'
    REQUIRED_FIELDS = ['emailid', 'name']
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=now)

    ACCOUNT_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('resort_owner', 'Resort Owner'),
    ]

    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, default='customer')
    email = models.EmailField(default='default@example.com')
    password = models.CharField(max_length=255)  # Store hashed password
    is_verified = models.BooleanField(default=False)  # To track email verification

    class Meta:
        db_table = 'users'
        unique_together = ('emailid', 'username')  # Ensure unique combination of email and username

    def get_email_field_name(self):
        return 'emailid'

    def __str__(self):
        return self.username

class Bookingpackage(models.Model):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, null=True)  
    num_adults = models.IntegerField(validators=[MinValueValidator(1)])
    num_children = models.IntegerField(validators=[MinValueValidator(0)])
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    package = models.ForeignKey(PackageManagement, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='credit_card')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now, editable=False)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.package}"

    class Meta:
        ordering = ['-booking_date']

    def save(self, *args, **kwargs):
        if not self.id:
            self.booking_date = timezone.now()
        return super(Bookingpackage, self).save(*args, **kwargs)





# Booking Package Model
class Bookingpackage(models.Model):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, null=True)  
    num_adults = models.IntegerField(validators=[MinValueValidator(1)])
    num_children = models.IntegerField(validators=[MinValueValidator(0)])
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    package = models.ForeignKey(PackageManagement, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now, editable=False)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    num_rooms = models.IntegerField(default=1)
    food_preference = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.package}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.booking_date = timezone.now()  # Automatically set the booking date
        return super(Bookingpackage, self).save(*args, **kwargs)
