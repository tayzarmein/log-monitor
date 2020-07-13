from django.db import models

class Gclog(models.Model):
    id = models.BigAutoField(primary_key=True)
    logtype = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    newgenbefore = models.IntegerField(db_column='newGenBefore', blank=True, null=True)  # Field name made lowercase.
    newgen = models.IntegerField(db_column='newGen', blank=True, null=True)  # Field name made lowercase.
    newgentotal = models.IntegerField(db_column='newGenTotal', blank=True, null=True)  # Field name made lowercase.
    oldgenbefore = models.IntegerField(db_column='oldgenBefore', blank=True, null=True)  # Field name made lowercase.
    oldgen = models.IntegerField(db_column='oldGen', blank=True, null=True)  # Field name made lowercase.
    oldgentotal = models.IntegerField(db_column='oldGenTotal', blank=True, null=True)  # Field name made lowercase.
    newplusoldbefore = models.IntegerField(db_column='newPlusOldBefore', blank=True, null=True)  # Field name made lowercase.
    newplusold = models.IntegerField(db_column='newPlusOld', blank=True, null=True)  # Field name made lowercase.
    newplusoldtotal = models.IntegerField(db_column='newPlusOldTotal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gclog'

