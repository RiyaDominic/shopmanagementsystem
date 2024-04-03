from django.db import models

# Create your models here.
class Products(models.Model):
    Product_category = models.CharField(max_length=255,choices=(
        ("measuring tools","measuring tools"),
        ("Striking tools","Striking tools"),
        ("Metal cutting tools",'Metal cutting tools'),
        ("Holding tools","Holding tools"),
        ("Sharpening tools","Sharpening tools"),
        ("grinding tools","grinding tools"),
        ("Other","Other")
    )                       
                                        )
    Product_Name = models.CharField(max_length=255)
    Product_unit_Price = models.CharField(max_length=255)
    GST = models.CharField(max_length=255)
    Product_Brand = models.CharField(max_length=255)
    Product_Stock = models.CharField(max_length=255)
    Batch_Code = models.CharField(max_length=255)
    product_Image = models.FileField(upload_to="product_image")
    Expairy_Date = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return str(self.Product_Name +" " +self.Product_Brand)
    
    
