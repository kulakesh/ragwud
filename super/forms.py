from django import forms
from .models import Product, Category

class ProductCreateForm(forms.ModelForm):
    description = forms.CharField(required=False)
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'image']
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.order_by("name")
        self.fields["category"].empty_label = "Select category"
    
    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("Category is required.")

        return category
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name.strip()) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")

        return name
    
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise forms.ValidationError("Product image is required.")

        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 2MB.")

        return image
    
class ProductUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'image']
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.order_by("name")
        self.fields["category"].empty_label = "Select category"

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("Category is required.")

        return category
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name.strip()) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")

        return name
    
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 2MB.")

        return image
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name.strip()) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")

        return name