from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Cart



def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")




def courses(request):
    courses = Course.objects.all()
    return render(request, "course.html", {'courses': courses})




# ADD TO CART
@login_required
def add_to_cart(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    # ⭐ check already exists
    cart_item = Cart.objects.filter(
        user=request.user,
        course=course
    ).first()

    if cart_item:
        # already added → go to cart page
        return redirect('cart')

    # add new item
    Cart.objects.create(
        user=request.user,
        course=course
    )

    return redirect('cart')


# CART PAGE
@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(int(item.course.price) for item in cart_items)

    context = {
        'courses': [item.course for item in cart_items],
        'total': total
    }

    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, id):

    course = get_object_or_404(Course, id=id)

    Cart.objects.filter(
        user=request.user,
        course=course
    ).delete()

    return redirect('cart')