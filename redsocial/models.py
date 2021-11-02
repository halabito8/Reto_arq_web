from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo
from djongo import models

# Create your models here.

# Modelos de MongoDB
class Comments(models.Model):
    comment = models.CharField(max_length=100)
    user = models.IntegerField()

    class Meta:
        abstract = True

class Posts(models.Model):
    text = models.CharField(max_length=100)
    user = models.IntegerField()

    comments = models.EmbeddedField(model_container=Comments, null=True)

# Modelos Neo4j

class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    # Relations :
    friends = RelationshipTo('Person','FRIEND')

