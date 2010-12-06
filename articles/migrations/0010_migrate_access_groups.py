# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

"""
for c in Category.objects.all():
    groups = Group.objects.filter(article__in=c.article_set.all()).distinct()
    if groups:
        if c.article_set.filter(access_groups__isnull=True):
            print "Adding groups %s to %s" % (', '.join([g.name for g in groups]), c.name)
            for g in groups:
                c.access_groups.add(g)
            #c.save()
        else:
            print "Category %s has articles with access groups but not all articles have access groups set" % (c.name,)

def intranet_user_from_user(user):
    intranetuser = IntranetUser(user_ptr=user)
    for f in User._meta.fields:
        setattr(intranetuser, f.name, getattr(user, f.name))
    intranetuser.save()
for u in User.objects.filter(intranetuser__isnull=True): intranet_user_from_user(u)
"""

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        #for c in Category.objects.all(): 
        #    print Group.objects.filter(article__in=Article.objects.filter(category__in=c.get_descendants(True)))


        for c in orm['articles.category'].objects.all():
            groups = orm['auth.group'].objects.filter(article__in=c.article_set.all())distinct()
            #groups = orm['auth.group'].objects.filter(article__in=orm['articles.article'].objects.filter(
            #    category__in=c.objects.filter(tree_id=c.tree_id, lft__range=(c.lft, c.rght))))distinct()
            if groups:
                print "Adding groups %s to %s" % (', '.join([g.name for g in groups]), c.name)
                for g in groups:
                    c.access_groups.add(g)
                c.save()

    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'articles.article': {
            'Meta': {'ordering': "('-publication_date',)", 'unique_together': "(('category', 'slug'),)", 'object_name': 'Article'},
            'access_groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('incuna.db.models.AutoSlugField.AutoSlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255', 'populate_from': "'title'", 'field_separator': "u'-'"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'null': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'articles.category': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Category'},
            'access_groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'calendar_id': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_by': ('django.db.models.fields.CharField', [], {'default': "'-publication_date'", 'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['articles.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('incuna.db.models.AutoSlugField.AutoSlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255', 'populate_from': "'name'", 'field_separator': "u'-'"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'articles.mediafilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'MediaFileContent', 'db_table': "'articles_article_mediafilecontent'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediafile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles_mediafilecontent_set'", 'to': "orm['medialibrary.MediaFile']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafilecontent_set'", 'to': "orm['articles.Article']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'articles.richtextcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RichTextContent', 'db_table': "'articles_article_richtextcontent'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextcontent_set'", 'to': "orm['articles.Article']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'medialibrary.category': {
            'Meta': {'ordering': "['parent__title', 'title']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['medialibrary.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'medialibrary.mediafile': {
            'Meta': {'object_name': 'MediaFile'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['medialibrary.Category']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['articles']
