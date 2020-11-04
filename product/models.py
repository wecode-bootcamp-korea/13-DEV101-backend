from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name     = models.CharField(max_length=20)

    class Meta:
        db_table = 'sub_categories'

class Coupon(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'coupons'

class Level(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'levels'

class Product(models.Model):
    name           = models.CharField(max_length=200)
    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category   = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    creator        = models.ForeignKey('user.Creator', on_delete=models.CASCADE)
    level          = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    coupon         = models.ForeignKey(Coupon, on_delete=models.SET_DEFAULT, default=0)
    price          = models.DecimalField(max_digits=16, decimal_places=2)
    discount       = models.DecimalField(max_digits=3, decimal_places=2)
    chapter        = models.PositiveIntegerField(default=1)
    chapter_detail = models.PositiveIntegerField(default=0)
    subtitle_flag  = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    is_checked     = models.BooleanField(default=True)
    is_open        = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'

class Tag(models.Model):
    name    = models.CharField(max_length=40)
    product = models.ManyToManyField(Product, through='ProductTag', related_name='tags')

    class Meta:
        db_table = 'tags'

class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag     = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_tags'

class Review(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    good_bad = models.BooleanField(null=True)
    content  = models.TextField()

    class Meta:
        db_table = 'reviews'

class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'

class ProductLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_likes'

class Post(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_likes'

class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

class Watched(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'watched'

class Introduction(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    theme_image_url     = models.URLField(max_length=2000)
    process_image_url   = models.URLField(max_length=2000)
    work_image_url      = models.URLField(max_length=2000)
    theme_description   = models.TextField()
    process_description = models.TextField()
    work_description    = models.TextField()

    class Meta:
        db_table = 'introductions'

class TitleCover(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    title               = models.CharField(max_length=200)
    cover_image_url     = models.URLField(max_length=2000)
    thumbnail_image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'title_covers'
        
class Survey(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    curriculum1 = models.TextField()
    curriculum2 = models.TextField()
    curriculum3 = models.TextField()
    curriculum4 = models.TextField()
    curriculum5 = models.TextField(null=True)
    curriculum6 = models.TextField(null=True)

    class Meta:
        db_table = 'surveys'

class BasicInfo(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category    = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category_detail = models.CharField(max_length=45)
    level           = models.ForeignKey(Level, on_delete=models.CASCADE)

    class Meta:
        db_table = 'basic_infos'

class Cheered(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cheered'

class Summary(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'summaries'

class SummaryTag(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE)
    name    = models.CharField(max_length=200)

    class Meta:
        db_table = 'summary_tags'

class ChannelType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'channel_types' 

class Channel(models.Model):
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    channel_type = models.ForeignKey(ChannelType, on_delete=models.CASCADE)
    name         = models.CharField(max_length=45)
    channel_url  = models.URLField(max_length=2000)

    class Meta:
        db_table = 'channels'

