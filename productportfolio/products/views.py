from django.shortcuts import render, get_object_or_404
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from .models import Product
import json

# Create your views here.
def home(r):
    products = Product.objects.all()
    product_images = [json.loads(prod.image.name)["images"][0] for prod in products]
    products_and_images = zip(product_images, products)
    return render(r, 'products/home.html', {"products": products_and_images})


def product(r, product):
    product_object = get_object_or_404(Product, name=product)
    images = json.loads(product_object.image.name)["images"]
    return render(r, 'products/productDetail.html', {'product': product_object, "images": images})


def admin_add_product(r):
    if r.method == "POST":
        if r.FILES.get("image") and r.POST.get("name") and r.POST.get("desc"): # check fields arent empty
            fs = FileSystemStorage() # used to save files
            images = dict(r.FILES)["image"] # get the image file
            image_names = [] # list of all image names
            for image in images:
                fs.save(image.name, image) # save image to the media file
                image_names.append(image.name) # add name to list
            query = Product(image=json.dumps({"images": image_names}), name=r.POST["name"], desc=r.POST["desc"])
            # create a new record with the image column as a json listing all image names
            query.save()
            return admin.site.urls[0][7].url_patterns[0].callback(r) # return to all products page
        else:
            return admin.site.urls[0][7].url_patterns[1].callback(r) # return to form, django will warn about missing fields
    elif r.method == "GET":
        return admin.site.urls[0][7].url_patterns[1].callback(r) # if it is a GET method, return the form
