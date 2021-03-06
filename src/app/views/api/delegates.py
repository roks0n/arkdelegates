from django.http import Http404
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from app.delegate_utils import fetch_delegates, fetch_new_delegates
from app.models import Delegate
from app.permissions import IsOwnerOrReadOnly
from app.serializers import DelegateInfo
from app.views.api.serializers import DelegateModelSerializer, DelegatePayoutModelSerializer


class Delegates(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, delegate_slug=None, wallet_address=None, *args, **kwargs):
        if wallet_address:
            # todo: support fetching delegate via wallet address
            raise Http404()
        elif delegate_slug:
            if not Delegate.objects.filter(slug=delegate_slug).exists():
                raise Http404()
            data = self._get_delegate(delegate_slug)
        else:
            data = self._get_delegates()
        return Response(data)

    def put(self, request, delegate_slug=None, wallet_address=None, **kwargs):
        if not delegate_slug and request.user.is_authenticated:
            delegate = get_object_or_404(Delegate, slug=request.user.delegate.slug)
        elif wallet_address:
            delegate = get_object_or_404(Delegate, address=wallet_address)
        else:
            delegate = get_object_or_404(Delegate, slug=delegate_slug)

        # Check permissions, if user has permissions to change data for a delegate
        if request.user.has_perm("app.payout_change"):
            serializer = DelegatePayoutModelSerializer(delegate, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            self.check_object_permissions(request, delegate)
            serializer = DelegateModelSerializer(delegate, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=201)

    def _get_delegate(self, delegate_slug):
        """
        Gets data for a specific delegate

        Args:
            delegate_slug (string): delegate slug

        Returns:
            json: JSON object containing all delegate information

        Raises:
            Http404: if delegate with given delegate slug does not exist
        """
        delegate_result = DelegateInfo.from_slug(delegate_slug).data
        return delegate_result

    def _get_delegates(self):
        """
        Gets all delegates. It shows up to 60 delegates per page.

        Returns:
            json: JSON object containing all delegates
        """
        page = int(self.request.GET.get("page", 1))
        limit = int(self.request.GET.get("limit", 60))
        latest_proposals = bool(self.request.GET.get("latest", 0))

        if latest_proposals:
            delegates, paginator = fetch_new_delegates(page, limit=limit)
        else:
            delegates, paginator = fetch_delegates(page, limit=limit)

        return {
            "all_results": paginator.paginator.count,
            "total_pages": paginator.paginator.num_pages,
            "current_page": page,
            "data": delegates,
        }
