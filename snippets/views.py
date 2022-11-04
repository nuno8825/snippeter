from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from snippets.forms import SnippetForm
from snippets.models import Snippet


@login_required
def top(request):
    snippets = Snippet.objects.all()
    user = request.user
    context = {"snippets": snippets, "dare": user}
    return render(request, "snippets/top.html", context)


@login_required
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form = SnippetForm()
    return render(request, "snippets/snippet_new.html", {'form': form})


@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません。")

    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippet_detail', snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'snippets/snippet_edit.html', {'form': form})


@login_required
def snippet_delete(request, snippet_id):  # 投稿の削除機能
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if request.method == "POST":
        snippet.delete()
        return redirect("top")
    return render(request, 'snippets/snippet_delete.html', {'snippet': snippet})


@login_required
def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    return render(request, 'snippets/snippet_detail.html',
                  {'snippet': snippet})
