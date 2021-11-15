from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo
from djongo import models

# Create your models here.

# Modelos de MongoDB
class Comments(models.Model):
    _id = models.ObjectIdField()
    comment = models.CharField(max_length=100)
    user = models.IntegerField()
    date = models.DateTimeField()

class Posts(models.Model):
    _id = models.ObjectIdField()
    text = models.CharField(max_length=100)
    user = models.CharField()

    comments = models.ArrayField(model_container=Comments, null=True)

# Modelos Neo4j

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)
    email = StringProperty()

    # Relations :
    friends = RelationshipTo('Person','FRIEND')

