from django.contrib.auth.decorators import user_passes_test


def staff_required(view_func):
    """관리자(is_staff=True) 사용자만 접근 가능"""
    decorated = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/accounts/login/'
    )(view_func)
    return decorated