# -*- coding: utf-8 -*-

from tournoi.models import Club


CLUBS = (('Bastia', 'SCB'),
         ('Bordeaux', 'FCGB'),
         ('Caen', 'SMC'),
         ('Évian-TG', 'ETG'),
         ('Guingamp', 'EAG'),
         ('Lens', 'RCL'),
         ('Lille', 'LOSC'),
         ('Lorient', 'FCL'),
         ('Lyon', 'OL'),
         ('Marseille', 'OM'),
         ('Metz', 'FCM'),
         ('Monaco', 'ASM'),
         ('Montpellier', 'MHSC'),
         ('Nantes', 'FCN'),
         ('Nice', 'OGCN'),
         ('Paris-SG', 'PSG'),
         ('Reims', 'SR'),
         ('Rennes', 'SRFC'),
         ('Saint-Étienne', 'ASSE'),
         ('Toulouse', 'TFC'))


for name, shortname in CLUBS:
   club = Club(name=name, shortname=shortname)
   club.save()
