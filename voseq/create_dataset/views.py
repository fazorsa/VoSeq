import logging
import os
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from core.utils import get_context
from .forms import CreateDatasetForm
from .utils import CreateDataset


log = logging.getLogger(__name__)


@login_required
def index(request):
    form = CreateDatasetForm()
    context = get_context(request)
    context["form"] = form

    return render(request, 'create_dataset/index.html', context)


@login_required
def results(request):
    context = get_context(request)

    if request.method == 'POST':
        form = CreateDatasetForm(request.POST)

        if form.is_valid():
            dataset_format = form.cleaned_data['file_format']
            dataset_creator = CreateDataset(form.cleaned_data)
            dataset = "{}{}{}".format(
                dataset_creator.dataset_str[0:1500],
                '\n...\n\n\n',
                '#######\nComplete dataset file available for download.\n#######',
            )
            errors = dataset_creator.errors
            warnings = set(dataset_creator.warnings)

            dataset_file_abs = dataset_creator.dataset_file
            if dataset_file_abs is not None:
                dataset_file = re.search(
                    '([A-Z]+_[a-z0-9]+\.txt)',
                    dataset_file_abs
                ).groups()[0]
            else:
                dataset_file = False

            context['dataset_file'] = dataset_file
            context['charset_block'] = dataset_creator.charset_block
            context['dataset'] = dataset
            context['dataset_format'] = dataset_format
            context['errors'] = errors
            context['warnings'] = warnings
            return render(request, 'create_dataset/results.html', context)
        else:
            log.debug("invalid form")
            context["form"] = form
            return render(request, 'create_dataset/index.html', context)
    else:
        return HttpResponseRedirect('/create_dataset/')


@login_required
def serve_file(request, file_name):
    final_name = guess_file_extension(file_name)
    cwd = os.path.dirname(__file__)
    dataset_file = os.path.join(cwd,
                                'dataset_files',
                                file_name,
                                )
    if os.path.isfile(dataset_file):
        response = HttpResponse(open(dataset_file, 'r').read(), content_type='application/text')
        response['Content-Disposition'] = 'attachment; filename={}'.format(final_name)
        os.remove(dataset_file)
        return response
    else:
        return render(request, 'create_dataset/missing_file.html')


def guess_file_extension(file_name):
    try:
        prefix = re.search('^(\w+)\_', file_name).group()
    except AttributeError:
        return file_name

    if prefix == 'MEGA_':
        extension = 'meg'
    else:
        return file_name

    name = file_name.replace('.txt', '')
    return '{0}.{1}'.format(name, extension)
