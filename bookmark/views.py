import bookmark
from django.shortcuts import get_object_or_404, render
from business.models import Business
from customer.models import Customer
from .models import Bookmark
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


# def bookmark_business(request,id):
#      bookmark = Bookmark.object.get(id=id)
#      business_id = bookmark.business.id

#      if business_id.filter(id=request.user.customer.id).exists():
#         business_id.remove(request.user.customer)

#      else:
#        business_id.add(request.user.customer)


#      return render(request, 'bookmark/showbookmark.html')


# #def bookmark_list(request):
