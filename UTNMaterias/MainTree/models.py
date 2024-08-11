from django.db import models


class UTNSubject(models.Model):
    name = models.CharField(max_length=100)
    approval_fathers = models.CharField(max_length=300, blank=True)
    approval_children = models.CharField(max_length=300, blank=True)
    regular_fathers = models.CharField(max_length=300, blank=True)
    regular_children = models.CharField(max_length=300, blank=True)
    year = models.IntegerField()
    # its necessary to approve all subjects that come before this one to approve it
    all_approved = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UTNSubjectSistemas(UTNSubject):
    pass


class UTNSubjectElectrica(UTNSubject):
    pass


class UTNSubjectElectronica(UTNSubject):
    pass


class UTNSubjectMecanica(UTNSubject):
    pass


class UTNSubjectMetalurgica(UTNSubject):
    pass


class UTNSubjectCivil(UTNSubject):
    pass


class UTNSubjectIndustrial(UTNSubject):
    pass


class UTNSubjectQuimica(UTNSubject):
    pass
