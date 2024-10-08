from django.urls import reverse
from django.conf import settings


def is_active(request, view_names):
    result = ''
    parts = request.path.split("/")
    if parts[2] != '':
        result = parts[2]
    else:
        result = 'dashboard'
    return any(result == view_name for view_name in view_names)


def has_permission(user, view_names):
    if settings.LOCAL:
        return True
    else:
        return any(user.has_permission(view_name) for view_name in view_names)


def generate_drawer(request, user):
    drawer = [
        {
            'section': 'Picking',
            'childs': [
                {
                    "name": "Dashboard",
                    "href": reverse('dashboard:index'),
                    "href_native": ['dashboard:index'],
                    "icon": "fas fa-tachometer-alt",
                    "active": is_active(request, ['dashboard'])
                },
                {
                    "name": "Poc Picking",
                    "icon": "fas fa-boxes",
                    "href": reverse('dashboard:invoices'),
                    "href_native": ['dashboard:invoices'],
                    "active": is_active(request, ['invoices']),
                },
                {
                    "name": "Moto Picking",
                    "icon": "fas fa-motorcycle",
                    "href": reverse('dashboard:picking'),
                    "href_native": ['dashboard:picking'],
                    "active": is_active(request, ['picking']),
                }
            ]
        },
        {
            'section': 'Configuración',
            'childs': [
                # {
                #     "name": "Puntos",
                #     "icon": "fas fa-coins",
                #     "href": reverse('dashboard:points'),
                #     "href_native": ['dashboard:points'],
                #     "active": is_active(request, ['points']),
                # },
                {
                    "name": "Configuración de clientes",
                    "icon": "fas fa-users-cog",
                    "href_native": ['dashboard:orders',
                                    'dashboard:clients'],
                    "active": is_active(request, ['orders',
                                                  'clients']),
                    "children": [
                        {
                            "name": "Clientes",
                            "icon": "fas fa-user",
                            "href": reverse('dashboard:clients'),
                            "href_native": ['dashboard:clients'],
                            "active": is_active(request, ['clients']),
                        },
                        {
                            "name": "Pedidos por Cliente",
                            "href": reverse('dashboard:orders'),
                            "href_native": ['dashboard:orders'],
                            "icon": "fas fa-shopping-cart",
                            "active": is_active(request, ['orders'])
                        }
                    ]
                },
                {
                    "name": "Configuración de tiendas",
                    "icon": "fas fa-shopping-bag",
                    "href_native": ['dashboard:cities',
                                    'dashboard:stores', 'dashboard:bottles', 'dashboard:bottle_rules'],
                    "active": is_active(request, ['cities',
                                                  'stores', 'bottles', 'bottle_rules']),
                    "children": [
                        {
                            "name": "Tiendas",
                            "icon": "fas fa-store",
                            "href": reverse('dashboard:stores'),
                            "href_native": ['dashboard:stores'],
                            "active": is_active(request, ['stores']),
                        },
                        {
                            "name": "Ciudades",
                            "href": reverse('dashboard:cities'),
                            "href_native": ['dashboard:cities'],
                            "icon": "fas fa-city",
                            "active": is_active(request, ['cities'])
                        },
                        {
                            "name": "Botellas",
                            "href": reverse('dashboard:bottles'),
                            "href_native": ['dashboard:bottles'],
                            "icon": "fas fa-wine-bottle",
                            "active": is_active(request, ['bottles'])
                        },
                        {
                            "name": "Reglas de Botellas",
                            "href": reverse('dashboard:bottle_rules'),
                            "href_native": ['dashboard:bottle_rules'],
                            "icon": "fas fa-balance-scale",
                            "active": is_active(request, ['bottle_rules'])
                        }
                    ]
                },
                {
                    "name": "Items a Clientes",
                    "icon": "fas fa-box-open",
                    "href_native": ['dashboard:products',
                                    'dashboard:stocks'],
                    "active": is_active(request, ['products',
                                                  'stocks']),
                    "children": [
                        {
                            "name": "Cupones",
                            "icon": "fas fa-gift",
                            "href": reverse('dashboard:products'),
                            "href_native": ['dashboard:products'],
                            "active": is_active(request, ['products']),
                        },
                        {
                            "name": "Stock",
                            "href": reverse('dashboard:stocks'),
                            "href_native": ['dashboard:stocks'],
                            "icon": "fas fa-warehouse",
                            "active": is_active(request, ['stocks'])
                        }
                    ]
                },
                {
                    "name": "Accesos",
                    "icon": "fas fa-sign-in-alt",
                    "href_native": ['dashboard:users',
                                    'dashboard:roles'],
                    "active": is_active(request, ['users',
                                                  'roles']),
                    "children": [
                        {
                            "name": "Roles",
                            "href": reverse('dashboard:roles'),
                            "href_native": ['dashboard:roles'],
                            "icon": "fas fa-user-cog",
                            "active": is_active(request, ['roles'])
                        },
                        {
                            "name": "Usuarios",
                            "href": reverse('dashboard:users'),
                            "href_native": ['dashboard:users'],
                            "icon": "fas fa-users",
                            "active": is_active(request, ['users']),
                        },

                    ]
                }
            ]
        }
    ]

    filtered_drawer = []
    flag = True
    for section in drawer:
        section_children = []
        for index, item in enumerate(section['childs']):
            if index == 0 and flag:
                section_children.append(item)
                flag = False
                continue
            if 'children' in item:
                children = []
                for child in item['children']:
                    if has_permission(user, child['href_native']):
                        children.append(child)
                if children:
                    item['children'] = children
                    section_children.append(item)
            else:
                if has_permission(user, item['href_native']):
                    section_children.append(item)
        if section_children:
            section['childs'] = section_children
            filtered_drawer.append(section)

    return filtered_drawer


def drawer(request):
    user = request.user
    if user.is_authenticated:
        filtered_drawer = generate_drawer(request, user)
        return {'drawer': filtered_drawer}
    else:
        return {}
