from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Material, MaterialInstance, MaterialInstanceHistory
from .forms import MaterialrModelForm, MaterialModelFormCount, MaterialInstanceForm

import datetime

today = datetime.datetime.today()

def dashboard_page(request):
    all_materials = Material.objects.all()

    # collect and calculate how many materials need to refill

    material_need_to_by = []

    for material in all_materials:
        current_count = material.count
        max_count = material.count_full

        procentage = (int(current_count) / int(max_count) ) * 100
        # print(procentage)

        if procentage < 30:
            material_need_to_by.append(material.pk)

    # print(len(material_need_to_by))
    try:
        materials_need_to_by_vs_all = 100 - (100 / (int(all_materials.count() / len(material_need_to_by))))
        # print(materials_need_to_by_vs_all)
    except Exception:
        materials_need_to_by_vs_all = 100
        pass

    # count of deleted materials instances in this month
    deleted_materials_instance_in_this_mont = MaterialInstanceHistory.objects.filter(created__year=today.year,
                                                                                     created__month=today.month)
    deleted_materials_instance_in_this_mont_sum = deleted_materials_instance_in_this_mont.aggregate(Sum('count_deleted'))

    #procent generate for count of material
    procentages_materials = {}
    # print(all_materials)
    for m in all_materials:
        try:
            m.procent = 100 / (int(m.count_full) / int(m.count))
            print(m)
        except Exception:
            m.procent = 100
            pass
    print(procentages_materials)

    # generate main context
    context = {
        'materials': all_materials,
        'materials_count': all_materials.count(),
        'materials_need_to_by': len(material_need_to_by),
        'materials_need_to_by_vs_all': int(materials_need_to_by_vs_all),
        'deleted_materials_instance_in_this_mont': int(deleted_materials_instance_in_this_mont_sum['count_deleted__sum']),

    }
    return render(request, 'materials/dashboard.html', context)


class MaterialCreate(CreateView):
    model = Material
    form_class = MaterialrModelForm
    template_name = 'materials/material_create.html'
    success_url = reverse_lazy('materials:index')


class MaterialList(ListView):
    model = Material
    template_name = 'materials/material_list.html'
    context_object_name = 'instance'
    # paginate_by = 3   # нужно разобраться с ошибкой ZeroDivisionError: division by zero

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        for material in context['object_list']:
            material_count_current = material.count
            material_count_max = material.count_full
            print(f"{material.name} instance количество = " + str(material_count_current))
            print(f"{material.name} instance максимальное количество = " + str(material_count_max))

            count_procentage = (material_count_current / material_count_max) * 100
            print(f"{material.name} instance процент = " + str(int(count_procentage)) + " %")
            if 30 > count_procentage:

                print('count procentage less then meterial_count ' + str(material_count_current))
                context['need'] = False

                return context
            else:
                context['need'] = True
                return context
        return context


class MaterialUpdate(UpdateView):
    """
        Controller for update material fields
    """
    model = Material
    form_class = MaterialrModelForm
    template_name = 'materials/material_update_all.html'
    success_url = reverse_lazy('materials:index')


class MaterialUpdateCount(UpdateView):
    """
        Controller to change count of material for graf
    """
    model = Material
    form_class = MaterialModelFormCount
    template_name = 'materials/material_update_count.html'
    success_url = reverse_lazy('materials:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['graf'] = [12, 13, 26, 46]
        return context


class MaterialInstanceAdd(CreateView):
    """
        Controller for add material instance objects - count of exist material
    """
    model = MaterialInstance
    form_class = MaterialInstanceForm
    template_name = 'materials/material_instance_add.html'
    success_url = reverse_lazy('materials:index')

    def post(self, request, *args, **kwargs):
        post_instance_count = self.request.POST['instance_count']
        post_material = self.request.POST['material']
        print("Material instance " + post_material + " add " + post_instance_count)

        material = Material.objects.get(pk=post_material)

        materialinstance_current_count = MaterialInstance.objects.filter(material=material).count()

        for x in range(int(post_instance_count)):
            new_material_instance = MaterialInstance.objects.create(material=material)
            new_material_instance.save()
            print(new_material_instance)

        material.count = materialinstance_current_count + int(post_instance_count)
        material.save()

        return HttpResponseRedirect(self.success_url)


class MaterialInstanceDel(CreateView):
    """
        Controller for delete material instance objects
    """
    model = MaterialInstance
    form_class = MaterialInstanceForm
    template_name = 'materials/material_instance_del.html'
    success_url = reverse_lazy('materials:index')

    # take post request
    def post(self, request, *args, **kwargs):
        post_instance_count = self.request.POST['instance_count']
        post_material = self.request.POST['material']
        print("Material instance " + post_material + " DEL " + post_instance_count)

        material = Material.objects.get(pk=post_material)
        print(material)

        # get all material instance objects
        material_instance_objects = MaterialInstance.objects.filter(material=material)
        material_instance_objects_count = MaterialInstance.objects.filter(material=material).count() # get count objects
        # print(material_instance_objects_count)

        # get id all objects
        all_material_instance_id = material_instance_objects.values_list('pk', flat=True).order_by('pk')
        print(all_material_instance_id)

        # del all count objects
        for x in list(all_material_instance_id)[:int(post_instance_count)]:
            material_instance_to_del = MaterialInstance.objects.get(pk=x).delete()
            print(f"Deleted instance {material_instance_to_del}. Material - {material}")

        # change material count filed value
        material.count = int(material_instance_objects_count) - int(post_instance_count)
        material.save()

        # add record deletation of instances
        material_instance_history = MaterialInstanceHistory.objects.create(material=material, count_deleted=int(post_instance_count))
        material_instance_history.save()

        print(f'Deleted {post_instance_count} in material {material}')

        return HttpResponseRedirect(self.success_url)