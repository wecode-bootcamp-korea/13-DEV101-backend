import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE",'dev101.settings')
django.setup()

from user.models    import User,Creator
from product.models import *

CSV_PATH_USER    = '../dev101_files/user2.csv'
CSV_PATH_CREATOR = '../dev101_files/creator.csv'
CSV_PATH_CHANNEL = '../dev101_files/channel.csv'

#with open (CSV_PATH_USER) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader,None)
#    for row in data_reader:
#        #print(row)
#        User(
#            name = row[1],
#            email = row[0],
#            password = row[2],
#            phone_number = row[3],
#            image_url = row[4],
#            is_active = row[5],
#            cheered_point = row[6]
#        ).save()

#with open (CSV_PATH_CREATOR) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader,None)
#    for row in data_reader:
#        Creator(
#            image_url    = row[0],
#            nickname     = row[1],
#            introduction = row[2]
#        ).save()

with open (CSV_PATH_CHANNEL) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)

    for row in data_reader:

        #product_id = Product.objects.get(id=row[0]).id
        #channel_type_id = ChannelType.objects.get(id=row[1]).id
#        Channel(
#            name         = row[2],
#            url          = row[3],
#            channel_type_id = ChannelType.objects.get(id=row[1]).id,
#            product_id      = Product.objects.get(id=row[0]).id
#       ).save()

#        Summary(
#            product_id = Product.objects.get(id=row[0]).id,
#            image      = row[4]
#        ).save()

#        summary_id = Summary.objects.get(product_id=product_id).id
#        class_tags = row[5:]
#        for tag in class_tags:
#        #    print(summary_id,tag)
#            ClassTag(
#                summary_id = summary_id,
#                name       = tag
#            ).save()

#        user_id = row[8]
#        product_id = Product.objects.get(id=row[0]).id
#        Cheered(
#            product_id = product_id,
#            user_id    = user_id
#        ).save()

#        product_id = Product.objects.get(id=row[0]).id
#        product_category = Product.objects.get(id=row[0]).category.id
#        product_subcategory = Product.objects.get(id=row[0]).sub_category.id
#        #print(product_id,product_category,product_subcategory)
#        category_detail = row[9]
#        level = row[10]
#        BasicInfo(
#            product_id      = product_id,
#            category_id     = product_category,
#            sub_category_id = product_subcategory,
#            category_detail = category_detail,
#            level_id        = level
#        ).save()

        product_id = Product.objects.get(id=row[0]).id
        Survey(
            product_id  = product_id,
            curriculum1 = row[11],
            curriculum2 = row[12],
            curriculum3 = row[13],
            curriculum4 = row[14]
        ).save()
