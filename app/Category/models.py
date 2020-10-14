from django.db import models

# Create your models here.
## !Complete!
class Categories (models.Model):
    shop_no
    category_no
    category_depth
    parent_category_no
    category_name
    display_type
    full_category_name
    full_category_no
    root_category_no
    use_main
    use_display
    display_order
    soldout_product_display
    sub_category_product_display	
    hashtag_product_display
    hash_tags
    product_display_scope	
    product_display_type
    product_display_key	
    product_display_sort
    product_display_period
    normal_product_display_type
    normal_product_display_key
    normal_product_display_sort
    normal_product_display_period
    recommend_product_display_type
    recommend_product_display_key
    recommend_product_display_sort
    recommend_product_display_period
    new_product_display_type
    new_product_display_key
    new_product_display_sort
    new_product_display_period
    access_authority

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_category'
        verbose_name = '카테고리'
        vebose_name_plural = '카테고리'

class CategoriesDecorationimages(models.Model):
    shop_no
    category_no
    use_menu_image_pc	
    menu_image_pc
    menu_over_image_pc
    use_top_image_pc
    top_images_pc
    use_title_image_pc	
    title_image_pc
    use_menu_image_mobile
    menu_image_mobile
    use_top_image_mobile
    top_images_mobile
    use_title_image_mobile
    title_image_mobile

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_category'
        verbose_name = '카테고리'
        vebose_name_plural = '카테고리'

class CategoriesSeo(models.Model):
    shop_no
    category_no
    search_engine_exposure
    meta_title
    meta_author
    meta_description
    meta_keywords

    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_category'
        verbose_name = '카테고리'
        vebose_name_plural = '카테고리'

class Mains(models.Model):
    shop_no
    module_code
    display_group
    group_name
    soldout_sort_type	

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_category'
        verbose_name = '카테고리'
        vebose_name_plural = '카테고리'        
