# -*- coding: utf-8 -*-
#
#   Author: Cristian Salamea - ovnicraft@gmail.com
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from django.contrib.gis.utils import LayerMapping
from models import Emprendimiento, Provincia, Canton, Parroquia

e_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/POBLADOS/poblados.shp'))
    
def load_emprendimientos(verbose=True):
    lm = LayerMapping(Emprendimiento, e_shp, Emprendimiento.mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

p_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/PROVINCIAS/NACIONAL_POR_PROVINCIAS.shp'))

def load_provincias(verbose=True):
    lm = LayerMapping(Provincia, p_shp, Provincia.mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

c_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/CANTONES/NACIONAL_POR_CANTONES.shp'))

def load_cantones(verbose=True):
    lm = LayerMapping(Canton, c_shp, Canton.mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

pa_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/PARROQUIAS/NACIONAL_POR_PARROQUIAS.shp'))

def load_parroquias(verbose=True):
    lm = LayerMapping(Parroquia, pa_shp, Parroquia.mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)


