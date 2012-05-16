/*
[ tagSet with coma separator
overlay url
optional tags {"key":"value","key2":""}
]
*/
overlays=[
    // quartier
    ["type=boundary,boundary=administrative,admin_level=10"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/admin10/"],
    // commune
    ["type=boundary,boundary=administrative,admin_level=8"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/admin8/"],
    // arrondissement
    ["type=boundary,boundary=administrative,admin_level=7"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/admin7/"],
    // département
    ["type=boundary,boundary=administrative,admin_level=6"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/admin6/",
      {"name":"","wikipedia":"","website":"", "source":""}
    ],
    // ?
    ["type=boundary,boundary=administrative,admin_level=5"  
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/boundary_local_authority/"],
    // région
    ["type=boundary,boundary=administrative,admin_level=4"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/admin4/",
      {"name":"","wikipedia":"","website":"", "source":""}
    ],
    // communauté de commune
    ["type=boundary,boundary=local_authority,local_authority:FR=CC"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/boundary_local_authority/",
      {"name":"","ref:INSEE":"","wikipedia":"","website":"", "source":""}
    ],
    // communauté d'agglomération'
    ["type=boundary,boundary=local_authority,local_authority:FR=CA"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/boundary_local_authority/",
      {"name":"","ref:INSEE":"","wikipedia":"","website":"", "source":""}
    ],
    // communauté urbaine
    ["type=boundary,boundary=local_authority,local_authority:FR=CU"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/boundary_local_authority/",
      {"name":"","ref:INSEE":"","wikipedia":"","website":"", "source":""}
    ],
    // canton
    ["type=boundary,boundary=political,political_division=canton"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/boundary_political/",
      {"name":"","wikipedia":"","website":"", "source":""}
    ],
    // Circonscriptions législatives
    ["type=boundary,boundary=political,political_division=circonscription_législative"
    ,"http://layers.openstreetmap.fr/tiles/renderer.py/boundary_political/"],
    // Paroisses catho
    ["type=boundary,boundary=religious_administration,religion=christian,denomination=catholic,admin_level=8"
    ,undefined,
      {"name":"","ref:CEF":"","contact:phone":"","contact:email":"","website":""},
    ],
    // Zone pastorale catho
    ["type=boundary,boundary=religious_administration,religion=christian,denomination=catholic,admin_level=7"
    ,undefined,
      {"name":"","ref:CEF":"","contact:phone":"","contact:email":"","website":""},
    ],
    // Diocèse catho
    ["type=boundary,boundary=religious_administration,religion=christian,denomination=catholic,admin_level=6"
    ,undefined,
      {"name":"","ref:CEF":"","contact:phone":"","contact:email":"","website":"","wikipedia":""},
    ],
]
