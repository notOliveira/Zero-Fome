from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Organization, OrganizationProfile
from .forms import OrganizationCreationForm, OrganizationUpdateForm, OrganizationProfileUpdateForm

@login_required(login_url='/login')
def organizations(request):
    orgs_profile = OrganizationProfile.objects.select_related('organization').filter(organization__users=request.user)
    context = {
        'orgs': orgs_profile
    }
    return render(request, 'organizations/organizations.html', context)



@login_required(login_url='/login')
def create_org(request):
    if request.method == "POST":
        form = OrganizationCreationForm(request.POST)
        if form.is_valid():
            try:
                organization = form.save(commit=False)
                organization.save()
                form.save_m2m()
                organization.users.add(request.user)
                messages.success(request, 'Organização criada com sucesso!')
                return redirect('organizations')
            except Exception as e:
                messages.error(request, f'Houve um problema ao criar a organização: {str(e)}')
                return redirect('create-org')
        else:
            messages.error(request, 'Houve um problema ao validar o formulário. Por favor, tente novamente.')
            return redirect('create-org')
        
    return render(request, 'organizations/create-org.html', context={'form': OrganizationCreationForm()})

@login_required(login_url='/login')
def organization(request, id):
    organization_profile = get_object_or_404(OrganizationProfile, organization__id=id)

    if not organization_profile.organization.users.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')

    context = {
        'org': organization_profile
    }
    return render(request, 'organizations/organization.html', context)


def settings_org(request, id):
    if request.method == "POST":
        org_form = OrganizationUpdateForm(request.POST, instance=Organization.objects.filter(id=id).first())
        org_profile_form = OrganizationProfileUpdateForm(request.POST, request.FILES, instance=OrganizationProfile.objects.get(organization__id=id))
        if org_form.is_valid() and org_profile_form.is_valid():
            org_form.save()
            org_profile_form.save()
            messages.success(request, 'Configurações atualizadas com sucesso!')
            return redirect('settings-org', id=id)
        else:
            messages.error(request, 'Erro ao atualizar as configurações. Por favor, corrija os erros abaixo.')
    
    organization = Organization.objects.get(id=id)
    
    if request.user not in organization.users.all():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')
    
    organization_profile = OrganizationProfile.objects.get(organization=organization)
    
    context = {
        'org' : organization,
        'org_profile': organization_profile,
        'form_org': OrganizationUpdateForm(),
        'form_org_profile': OrganizationProfileUpdateForm(instance=organization_profile)
    }
    return render(request, 'organizations/settings-org.html', context)