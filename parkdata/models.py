# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# models of predicted data (not in used), version 1
class Finetreepredict(models.Model):
    blockid = models.IntegerField(db_column='BlockId')  # Field name made lowercase.
    period_h = models.IntegerField(db_column='Period_h')  # Field name made lowercase.
    period_m = models.IntegerField(db_column='Period_m')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    predicted = models.FloatField(db_column='Predicted')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FineTreePredict'

# models for realtime data
class Parking(models.Model):
    bay_id = models.IntegerField()
    lat = models.CharField(max_length=25)
    lon = models.CharField(max_length=25)
    st_market_id = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    parkingdate = models.DateTimeField(db_column='ParkingDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Parking'


class Weekly1(models.Model):
    blockid = models.IntegerField(db_column='BlockId')  # Field name made lowercase.
    period_h = models.IntegerField(db_column='Period_h')  # Field name made lowercase.
    period_m = models.IntegerField(db_column='Period_m')  # Field name made lowercase.
    volume = models.FloatField(db_column='Volume')  # Field name made lowercase.
    weekday = models.IntegerField(db_column='Weekday')  # Field name made lowercase.
    predicted = models.FloatField(db_column='Predicted')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Weekly1'

# models for predicted data (in use),version2
class Weekly2(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    blockid = models.IntegerField(db_column='BlockId')  # Field name made lowercase.
    period = models.IntegerField(db_column='Period')  # Field name made lowercase.
    weekday = models.IntegerField(db_column='Weekday')  # Field name made lowercase.
    prob = models.FloatField(db_column='Prob')  # Field name made lowercase.
    predicted = models.FloatField(db_column='Predicted')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Weekly2'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

# models for look up table
class Blockquery(models.Model):
    deviceid = models.IntegerField(db_column='DeviceId')  # Field name made lowercase.
    streemarker = models.CharField(db_column='StreeMarker', max_length=40)  # Field name made lowercase.
    blockid = models.IntegerField(db_column='BlockId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'blockQuery'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

# models for historical data in friday
class Lastfridata(models.Model):
    id = models.IntegerField(primary_key=True)
    bay_id = models.IntegerField()
    occupiedrate = models.FloatField(db_column='occupiedRate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lastFriData'

# models for historical data in monday
class Lastmondata(models.Model):
    id = models.IntegerField(primary_key=True)
    bay_id = models.IntegerField()
    occupiedrate = models.FloatField(db_column='occupiedRate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lastMonData'

# models for historical data in saturday
class Lastsatdata(models.Model):
    id = models.IntegerField(primary_key=True)
    bay_id = models.IntegerField()
    occupiedrate = models.FloatField(db_column='occupiedRate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lastSatData'

# models for historical data in sunday
class Lastsundata(models.Model):
    id = models.IntegerField(primary_key=True)
    bay_id = models.IntegerField()
    occupiedrate = models.FloatField(db_column='occupiedRate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lastSunData'

# models for historical data in thursday
class Lastthudata(models.Model):
    id = models.IntegerField(primary_key=True)
    bay_id = models.IntegerField()
    occupiedrate = models.FloatField(db_column='occupiedRate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lastThuData'

# models for historical data in tuesday
class Lasttuedata(models.Model):
    id = models.IntegerField(primary_key=True)
    bay_id = models.IntegerField()
    occupiedrate = models.FloatField(db_column='occupiedRate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lastTueData'

# models for historical data in wednesday
class Lastweddata(models.Model):
    id = models.IntegerField(primary_key=True)
    bay_id = models.IntegerField()
    occupiedrate = models.FloatField(db_column='occupiedRate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lastWedData'
