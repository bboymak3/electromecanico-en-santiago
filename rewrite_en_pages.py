#!/usr/bin/env python3
"""
Comprehensive rewrite script for /en/ pages.
Reads Spanish source pages, translates to proper English,
and saves to /en/ directory structure.
Excludes blog pages.
"""

import os
import re
import html
import json

# ============================================================================
# COMUNA DATA - slug, display name, zone description
# ============================================================================
COMUNA_DATA = {
    'alhue': {'name': 'Alhué', 'zone': 'rural area west of Santiago', 'area': 'Alhué'},
    'buin': {'name': 'Buin', 'zone': 'southern metropolitan area', 'area': 'Buin'},
    'calera-de-tango': {'name': 'Calera de Tango', 'zone': 'southern metropolitan area', 'area': 'Calera de Tango'},
    'cerrillos': {'name': 'Cerrillos', 'zone': 'western Santiago', 'area': 'Cerrillos'},
    'cerro-navia': {'name': 'Cerro Navia', 'zone': 'western Santiago', 'area': 'Cerro Navia'},
    'colina': {'name': 'Colina', 'zone': 'northern metropolitan area', 'area': 'Colina'},
    'conchali': {'name': 'Conchalí', 'zone': 'northern Santiago', 'area': 'Conchalí'},
    'curacavi': {'name': 'Curacaví', 'zone': 'rural area west of Santiago', 'area': 'Curacaví'},
    'el-bosque': {'name': 'El Bosque', 'zone': 'southern Santiago', 'area': 'El Bosque'},
    'el-monte': {'name': 'El Monte', 'zone': 'southeastern metropolitan area', 'area': 'El Monte'},
    'estacion-central': {'name': 'Estación Central', 'zone': 'western Santiago', 'area': 'Estación Central'},
    'huechuraba': {'name': 'Huechuraba', 'zone': 'northern Santiago', 'area': 'Huechuraba'},
    'independencia': {'name': 'Independencia', 'zone': 'central Santiago', 'area': 'Independencia'},
    'isla-de-maipo': {'name': 'Isla de Maipo', 'zone': 'southwestern metropolitan area', 'area': 'Isla de Maipo'},
    'la-cisterna': {'name': 'La Cisterna', 'zone': 'southern Santiago', 'area': 'La Cisterna'},
    'la-florida': {'name': 'La Florida', 'zone': 'southeastern Santiago', 'area': 'La Florida'},
    'la-granja': {'name': 'La Granja', 'zone': 'southern Santiago', 'area': 'La Granja'},
    'la-pintana': {'name': 'La Pintana', 'zone': 'southern Santiago', 'area': 'La Pintana'},
    'la-reina': {'name': 'La Reina', 'zone': 'eastern Santiago', 'area': 'La Reina'},
    'lampa': {'name': 'Lampa', 'zone': 'northern metropolitan area', 'area': 'Lampa'},
    'las-condes': {'name': 'Las Condes', 'zone': 'eastern Santiago', 'area': 'Las Condes'},
    'lo-barnechea': {'name': 'Lo Barnechea', 'zone': 'northeastern Santiago', 'area': 'Lo Barnechea'},
    'lo-espejo': {'name': 'Lo Espejo', 'zone': 'southwestern Santiago', 'area': 'Lo Espejo'},
    'lo-prado': {'name': 'Lo Prado', 'zone': 'western Santiago', 'area': 'Lo Prado'},
    'macul': {'name': 'Macul', 'zone': 'central-eastern Santiago', 'area': 'Macul'},
    'maipu': {'name': 'Maipú', 'zone': 'western Santiago', 'area': 'Maipú'},
    'maria-pinto': {'name': 'María Pinto', 'zone': 'rural area west of Santiago', 'area': 'María Pinto'},
    'melipilla': {'name': 'Melipilla', 'zone': 'southwestern metropolitan area', 'area': 'Melipilla'},
    'nunoa': {'name': 'Ñuñoa', 'zone': 'central Santiago', 'area': 'Ñuñoa'},
    'padre-hurtado': {'name': 'Padre Hurtado', 'zone': 'southern metropolitan area', 'area': 'Padre Hurtado'},
    'paine': {'name': 'Paine', 'zone': 'southern metropolitan area', 'area': 'Paine'},
    'pedro-aguirre-cerda': {'name': 'Pedro Aguirre Cerda', 'zone': 'southern Santiago', 'area': 'Pedro Aguirre Cerda'},
    'penaflor': {'name': 'Peñaflor', 'zone': 'southwestern metropolitan area', 'area': 'Peñaflor'},
    'penalolen': {'name': 'Peñalolén', 'zone': 'eastern Santiago', 'area': 'Peñalolén'},
    'pirque': {'name': 'Pirque', 'zone': 'southeastern metropolitan area', 'area': 'Pirque'},
    'providencia': {'name': 'Providencia', 'zone': 'central-eastern Santiago', 'area': 'Providencia'},
    'pudahuel': {'name': 'Pudahuel', 'zone': 'northwestern Santiago', 'area': 'Pudahuel'},
    'puente-alto': {'name': 'Puente Alto', 'zone': 'southeastern Santiago', 'area': 'Puente Alto'},
    'quilicura': {'name': 'Quilicura', 'zone': 'northern Santiago', 'area': 'Quilicura'},
    'quinta-normal': {'name': 'Quinta Normal', 'zone': 'western Santiago', 'area': 'Quinta Normal'},
    'recoleta': {'name': 'Recoleta', 'zone': 'northern Santiago', 'area': 'Recoleta'},
    'renca': {'name': 'Renca', 'zone': 'northwestern Santiago', 'area': 'Renca'},
    'san-bernardo': {'name': 'San Bernardo', 'zone': 'southern Santiago', 'area': 'San Bernardo'},
    'san-joaquin': {'name': 'San Joaquín', 'zone': 'southern Santiago', 'area': 'San Joaquín'},
    'san-jose-de-maipo': {'name': 'San José de Maipo', 'zone': 'southeastern mountain area', 'area': 'San José de Maipo'},
    'san-miguel': {'name': 'San Miguel', 'zone': 'southern Santiago', 'area': 'San Miguel'},
    'san-pedro': {'name': 'San Pedro', 'zone': 'northern metropolitan area', 'area': 'San Pedro'},
    'san-ramon': {'name': 'San Ramón', 'zone': 'southern Santiago', 'area': 'San Ramón'},
    'santiago': {'name': 'Santiago', 'zone': 'central Santiago', 'area': 'Santiago Centro'},
    'talagante': {'name': 'Talagante', 'zone': 'southwestern metropolitan area', 'area': 'Talagante'},
    'tiltil': {'name': 'Tiltil', 'zone': 'northern metropolitan area', 'area': 'Tiltil'},
    'vitacura': {'name': 'Vitacura', 'zone': 'eastern Santiago', 'area': 'Vitacura'},
}

# ============================================================================
# VEHICULO DATA
# ============================================================================
VEHICULO_DATA = {
    'chevrolet-sail': {'name': 'Chevrolet Sail', 'type': 'compact sedan', 'brand': 'Chevrolet'},
    'chevrolet-sonic': {'name': 'Chevrolet Sonic', 'type': 'compact sedan', 'brand': 'Chevrolet'},
    'chevrolet-spark': {'name': 'Chevrolet Spark', 'type': 'city car', 'brand': 'Chevrolet'},
    'fiat-bravo-tjet': {'name': 'Fiat Bravo T-Jet', 'type': 'compact sedan', 'brand': 'Fiat'},
    'ford-ecosport': {'name': 'Ford EcoSport', 'type': 'compact SUV', 'brand': 'Ford'},
    'ford-fiesta': {'name': 'Ford Fiesta', 'type': 'compact sedan', 'brand': 'Ford'},
    'honda-city': {'name': 'Honda City', 'type': 'compact sedan', 'brand': 'Honda'},
    'honda-civic': {'name': 'Honda Civic', 'type': 'mid-size sedan', 'brand': 'Honda'},
    'honda-cr-v': {'name': 'Honda CR-V', 'type': 'SUV', 'brand': 'Honda'},
    'hyundai-accent': {'name': 'Hyundai Accent', 'type': 'compact sedan', 'brand': 'Hyundai'},
    'hyundai-grand-i10': {'name': 'Hyundai Grand i10', 'type': 'city car', 'brand': 'Hyundai'},
    'hyundai-tucson': {'name': 'Hyundai Tucson', 'type': 'SUV', 'brand': 'Hyundai'},
    'kia-morning': {'name': 'Kia Morning', 'type': 'city car', 'brand': 'Kia'},
    'kia-rio': {'name': 'Kia Rio', 'type': 'compact sedan', 'brand': 'Kia'},
    'mazda-3': {'name': 'Mazda 3', 'type': 'compact sedan', 'brand': 'Mazda'},
    'mazda-cx-5': {'name': 'Mazda CX-5', 'type': 'SUV', 'brand': 'Mazda'},
    'mg-3': {'name': 'MG 3', 'type': 'compact sedan', 'brand': 'MG'},
    'mg-zs': {'name': 'MG ZS', 'type': 'SUV', 'brand': 'MG'},
    'nissan-kicks': {'name': 'Nissan Kicks', 'type': 'compact SUV', 'brand': 'Nissan'},
    'nissan-versa': {'name': 'Nissan Versa', 'type': 'compact sedan', 'brand': 'Nissan'},
    'peugeot-208': {'name': 'Peugeot 208', 'type': 'compact sedan', 'brand': 'Peugeot'},
    'peugeot-3008': {'name': 'Peugeot 3008', 'type': 'SUV', 'brand': 'Peugeot'},
    'renault-duster': {'name': 'Renault Duster', 'type': 'SUV', 'brand': 'Renault'},
    'renault-logan': {'name': 'Renault Logan', 'type': 'compact sedan', 'brand': 'Renault'},
    'subaru-forester': {'name': 'Subaru Forester', 'type': 'SUV', 'brand': 'Subaru'},
    'subaru-xv': {'name': 'Subaru XV', 'type': 'compact SUV', 'brand': 'Subaru'},
    'suzuki-baleno': {'name': 'Suzuki Baleno', 'type': 'compact sedan', 'brand': 'Suzuki'},
    'suzuki-celerio': {'name': 'Suzuki Celerio', 'type': 'city car', 'brand': 'Suzuki'},
    'suzuki-swift': {'name': 'Suzuki Swift', 'type': 'compact hatchback', 'brand': 'Suzuki'},
    'toyota-corolla': {'name': 'Toyota Corolla', 'type': 'mid-size sedan', 'brand': 'Toyota'},
    'toyota-yaris': {'name': 'Toyota Yaris', 'type': 'compact sedan', 'brand': 'Toyota'},
    'volkswagen-gol': {'name': 'Volkswagen Gol', 'type': 'compact sedan', 'brand': 'Volkswagen'},
}

# ============================================================================
# SERVICIO DATA
# ============================================================================
SERVICIO_DATA = {
    'air-conditioning': {'name': 'Air Conditioning Service', 'es_name': 'aire-acondicionado-automotriz'},
    'oil-change-at-home': {'name': 'Oil Change at Home', 'es_name': 'cambio-de-aceite-a-domicilio'},
    'brake-repair-at-home': {'name': 'Brake Repair at Home', 'es_name': 'cambio-de-frenos-a-domicilio'},
    'auto-electrical-at-home': {'name': 'Auto Electrical at Home', 'es_name': 'electricidad-automotriz-a-domicilio'},
    'diagnostic-scan-at-home': {'name': 'Diagnostic Scan at Home', 'es_name': 'diagnostico-con-scanner-a-domicilio'},
    '24-hour-mechanic': {'name': '24-Hour Mechanic', 'es_name': 'mecanico-24-horas'},
    'emergency-mechanic': {'name': 'Emergency Mechanic', 'es_name': 'mecanico-de-emergencia'},
}

# ============================================================================
# MARCA DATA
# ============================================================================
MARCA_DATA = {
    'chevrolet-sonic': {'name': 'Chevrolet', 'es_name': 'chevrolet-sonic'},
    'ford-fiesta': {'name': 'Ford', 'es_name': 'ford-fiesta'},
    'honda-city': {'name': 'Honda', 'es_name': 'honda-city'},
    'hyundai-grand-i10': {'name': 'Hyundai', 'es_name': 'hyundai-grand-i10'},
    'renault-duster': {'name': 'Renault', 'es_name': 'renault-duster'},
    'renault-logan': {'name': 'Renault', 'es_name': 'renault-logan'},
    'subaru-forester': {'name': 'Subaru', 'es_name': 'subaru-forester'},
    'subaru-xv': {'name': 'Subaru', 'es_name': 'subaru-xv'},
    'suzuki-celerio': {'name': 'Suzuki', 'es_name': 'suzuki-celerio'},
}

# ============================================================================
# SPANISH TO ENGLISH REPLACEMENTS FOR COMUNA PAGES
# These are applied to the Spanish source to create proper English
# ============================================================================
COMUNA_REPLACEMENTS = [
    # Meta/Head replacements
    ('lang="es"', 'lang="en"'),
    # Nav items
    ('Mecánico a Domicilio', 'Mobile Mechanic'),
    ('Servicios', 'Services'),
    ('Comunas', 'Areas'),
    ('Quiénes Somos', 'About Us'),
    ('Contacto', 'Contact'),
    ('Vehiculos', 'Vehicles'),
    ('Privacidad', 'Privacy'),
    # Hero section
    ('Servicio Automotriz Integral', 'Complete Automotive Service'),
    ('MECÁNICO A DOMICILIO EN ', 'MOBILE MECHANIC IN '),
    ('Mecánico a Domicilio en ', 'Mobile Mechanic in '),
    ('Autos Reparados', 'Cars Repaired'),
    ('Años de Experiencia', 'Years of Experience'),
    ('Garantía de Servicio', 'Service Guarantee'),
    ('Cotizar por WhatsApp', 'Get a Quote on WhatsApp'),
    ('Ver Servicios', 'View Services'),
    # Google Profile section
    ('Ver Nuestro Perfil de Google', 'View Our Google Profile'),
    ('opiniones verificadas', 'verified reviews'),
    # SEO Section
    ('El Mejor', 'The Best'),
    ('Mecánico a Domicilio', 'Mobile Mechanic'),
    ('Solución Inmediata', 'Immediate Solution'),
    ('Taller Mecánico Cerca de Mí en', 'Auto Repair Shop Near Me in'),
    ('Servicio Profesional de', 'Professional'),
    ('y toda la Región Metropolitana', 'and the Entire Metropolitan Region'),
    # Oil change section
    ('Servicio Más Buscado', 'Most Popular Service'),
    ('Cambio de Aceite', 'Oil Change'),
    ('cambio de aceite cerca mio', 'oil change near me'),
    ('es tu mejor opción', 'is your best choice'),
    ('Nuestro servicio a domicilio incluye aceite sintético y semi-sintético de primera calidad, reemplazo de filtro y revisión completa de niveles. Sin filas, sin taller: vamos a tu casa u oficina con todo el equipamiento. Agenda en minutos por WhatsApp y mantiene tu motor protegido.',
     'Our mobile service includes premium synthetic and semi-synthetic oil, filter replacement, and a complete fluid level check. No lines, no shop visit needed: we come to your home or office with all the equipment. Schedule in minutes on WhatsApp and keep your engine protected.'),
    ('A Domicilio', 'Mobile Service'),
    ('Sintético Premium', 'Premium Synthetic'),
    ('Filtro Incluido', 'Filter Included'),
    ('Agenda Rápido', 'Quick Scheduling'),
    ('Agenda Tu Cambio de Aceite Ya', 'Schedule Your Oil Change Now'),
    # Featured services section
    ('Servicios Más Solicitados en', 'Most Requested Services in'),
    ('Los servicios que más necesitan los vecinos de', 'The services most needed by residents of'),
    ('Agenda rápido por WhatsApp', 'Schedule quickly on WhatsApp'),
    ('Cotizar', 'Get Quote'),
    # Service cards
    ('Aceites sintéticos y semi-sintéticos premium. Incluye filtro y revisión de niveles. A domicilio en', 'Premium synthetic and semi-synthetic oils. Includes filter and fluid level check. Mobile service in'),
    ('Pastillas, discos, líquido y ABS. Medición digital del espesor. Tu seguridad es primero en', 'Pads, rotors, brake fluid, and ABS. Digital thickness measurement. Your safety comes first in'),
    ('Diagnóstico eléctrico completo. Batería, alternador, motor de arranque y cableado a domicilio en', 'Complete electrical diagnosis. Battery, alternator, starter motor, and wiring at your doorstep in'),
    ('Diagnóstico computarizado sin adivinanzas. Interpretación de códigos y soluciones reales en', 'Computerized diagnostics with no guesswork. Code interpretation and real solutions in'),
    # Reviews section
    ('Lo que dicen nuestros clientes', 'What Our Customers Say'),
    ('Tu confianza es nuestra mejor carta de presentación. Lee las experiencias de quienes ya confían en nuestro trabajo.',
     'Your trust is our best recommendation. Read the experiences of those who already trust our work.'),
    # Marquee section
    ('Conectamos a propietarios de vehículos con especialistas en mantenciones, revisiones y reparaciones específicas de tu auto en donde lo necesites',
     'We connect vehicle owners with specialists in maintenance, inspections, and specific repairs for your car wherever you need it'),
    ('Atención a domicilio en las comunas de la RM', 'Mobile service across all areas of the Metropolitan Region'),
    ('Marca automotriz', 'Automotive brand'),
    # Services section
    ('Nuestros Servicios de Mecánica Automotriz', 'Our Automotive Repair Services'),
    ('Ofrecemos una solución completa para el mantenimiento y reparación de tu vehículo en', 'We offer a complete solution for the maintenance and repair of your vehicle in'),
    ('desde la mecánica básica hasta el diagnóstico avanzado.', 'from basic mechanics to advanced diagnostics.'),
    ('Mecánica General y Mantenimiento', 'General Mechanics & Maintenance'),
    ('Realizamos', 'We perform'),
    ('mantenimiento preventivo', 'preventive maintenance'),
    ('engrase general', 'general lubrication'),
    ('cambio de aceite', 'oil change'),
    ('revisión técnica', 'technical inspection'),
    ('para mantener tu auto en óptimas condiciones.', 'to keep your car in optimal condition.'),
    ('Cotizar Ahora', 'Get a Quote'),
    ('Electromecánica y Electricidad', 'Electromechanical & Electrical'),
    ('Expertos en', 'Experts in'),
    ('electricidad automotriz', 'auto electrical systems'),
    ('reparación de ECU', 'ECU repair'),
    ('diagnóstico de fallas eléctricas', 'electrical fault diagnosis'),
    ('sistema de inyección', 'fuel injection system'),
    ('Chapa y Pintura Automotriz', 'Bodywork & Paint'),
    ('Recuperamos la estética de tu vehículo con', 'We restore the appearance of your vehicle with'),
    ('reparación de carrocería', 'bodywork repair'),
    ('chapa y pintura', 'panel beating and painting'),
    ('reparación de interiores y tapicería', 'interior and upholstery repair'),
    ('Aire Acondicionado y Calefacción', 'Air Conditioning & Heating'),
    ('Reparación y mantenimiento de aire acondicionado auto', 'Auto AC repair and maintenance'),
    ('Carga de gas, reparación de', 'Gas recharge, repair of'),
    ('compresor', 'compressor'),
    ('radiador', 'radiator'),
    ('calefacción', 'heating system'),
    ('Frenos y Suspensión', 'Brakes & Suspension'),
    ('Garantizamos tu seguridad con la', 'We guarantee your safety with'),
    ('reparación de frenos', 'brake repair'),
    ('(discos, pastillas)', '(rotors, pads)'),
    ('suspensión', 'suspension'),
    ('(amortiguadores)', '(shock absorbers)'),
    ('dirección', 'steering'),
    ('Reparación de Transmisión', 'Transmission Repair'),
    ('Diagnóstico y reparación de', 'Diagnosis and repair of'),
    ('transmisiones manuales y automáticas', 'manual and automatic transmissions'),
    ('embrague', 'clutch'),
    ('caja de transferencia', 'transfer case'),
    ('diferencial', 'differential'),
    ('Sistema de Escape y Turbos', 'Exhaust System & Turbos'),
    ('Reparación y mantenimiento de', 'Repair and maintenance of'),
    ('escapes de autos', 'car exhaust systems'),
    ('reparación de turbos', 'turbo repair'),
    ('catalizador', 'catalytic converter'),
    ('silenciador', 'muffler'),
    ('Sistemas de Gas GNV/GLP', 'CNG/LPG Gas Systems'),
    ('Instalación, certificación y', 'Installation, certification, and'),
    ('reparación de sistemas de gas para vehículos', 'repair of vehicle gas systems'),
    ('Conversión y mantenimiento para un ahorro garantizado.', 'Conversion and maintenance for guaranteed savings.'),
    ('Diagnóstico Computarizado', 'Computerized Diagnostics'),
    ('Utilizando tecnología de', 'Using'),
    ('scanner automotriz', 'automotive scanner'),
    ('ofrecemos un', 'we offer'),
    ('diagnóstico avanzado de fallas', 'advanced fault diagnosis'),
    ('para identificar problemas a tiempo.', 'to identify problems early.'),
    ('Servicio a Domicilio', 'At-Home Service'),
    ('No puedes venir? Nosotros vamos a ti. Ofrecemos', "Can't make it to the shop? We come to you. We offer"),
    ('servicio mecánico a domicilio en', 'mobile mechanic service in'),
    ('auxilio en carretera', 'roadside assistance'),
    # Heating/Climate section
    ('Servicio Avanzado de Climatizacion y Calefaccion Automotriz 24/7 en', 'Advanced Automotive Climate Control and Heating Service 24/7 in'),
    # SEO detailed services section
    ('Servicios Mecanicos en', 'Mechanical Services in'),
    ('Todos los servicios automotrices que necesitas directamente en tu comuna, sin moverte de casa', 'All the automotive services you need right in your area, without leaving home'),
    ('Mecanico a Domicilio en', 'Mobile Mechanic in'),
    ('Scanner Automotriz en', 'Automotive Scanner in'),
    ('Frenos y Pastillas en', 'Brakes and Pads in'),
    ('Cambio de Aceite en', 'Oil Change in'),
    ('Alineamiento y Suspension en', 'Alignment and Suspension in'),
    ('Reparacion de Motores en', 'Engine Repair in'),
    ('Embrague y Correa de Distribucion en', 'Clutch and Timing Belt in'),
    ('Servicio de Bateria y Electricidad en', 'Battery and Electrical Service in'),
    ('Cambio de Bujias y Mantencion en', 'Spark Plug Replacement and Maintenance in'),
    ('Emergencias 24/7 y Taller Mecanico Cerca de Mi', '24/7 Emergencies and Auto Repair Shop Near Me'),
    ('Cotizar Servicio en', 'Get a Service Quote in'),
    # How it works section
    ('COMO FUNCIONA NUESTRO SERVICIO DE MECÁNICA A DOMICILIO', 'HOW OUR MOBILE MECHANIC SERVICE WORKS'),
    ('Nuestro proceso es simple, rápido y pensado para que no pierdas tiempo. Nos encargamos de todo: desde la cotización hasta la entrega de tu vehículo funcionando en perfectas condiciones.',
     'Our process is simple, fast, and designed so you don\'t waste time. We handle everything: from the quote to delivering your vehicle in perfect working condition.'),
    ('COTIZA', 'GET A QUOTE'),
    ('Escríbenos al WhatsApp y cotiza tu servicio en', 'Message us on WhatsApp and get a quote for your service in'),
    ('de forma rápida y sin compromiso.', 'quickly and with no obligation.'),
    ('AGENDA', 'SCHEDULE'),
    ('Elige el día y hora que más te acomode. Nuestro técnico llega a tu ubicación en', 'Choose the day and time that works best for you. Our technician arrives at your location in'),
    ('TU AUTO LISTO EN 2 HORAS', 'YOUR CAR READY IN 2 HOURS'),
    ('Sin filas, sin quedarte a pie. Tu vehículo reparado directamente en', 'No lines, no being stranded. Your vehicle repaired right in'),
    # Why choose us section
    ('Por Qué Elegirnos para tu Servicio Mecánico a Domicilio en', 'Why Choose Us for Your Mobile Mechanic Service in'),
    ('Técnicos calificados y verificados', 'Qualified and verified technicians'),
    ('Profesionales con experiencia comprobada y certificaciones.', 'Professionals with proven experience and certifications.'),
    ('Diagnóstico preciso y transparente', 'Accurate and transparent diagnosis'),
    ('Te explicamos cada falla antes de reparar.', 'We explain every issue before repairing.'),
    ('Servicio sin anticipos ni sorpresas', 'No upfront payments or surprises'),
    ('Solo pagas después de recibir el servicio.', 'You only pay after receiving the service.'),
    ('Cobertura total en', 'Full coverage in'),
    ('Atendemos las 52 comunas de Santiago.', 'We serve all 52 areas of Santiago.'),
    ('Más de 5.000 clientes atendidos', 'Over 5,000 customers served'),
    ('Calificación 4.9/5 en Google con 148+ reseñas.', '4.9/5 rating on Google with 148+ reviews.'),
    ('Servicio de emergencia 24/7', '24/7 emergency service'),
    ('Auxilio mecánico en la vía a cualquier hora.', 'Roadside mechanical assistance at any hour.'),
    ('Nuestro objetivo es que tengas la seguridad de estar en manos profesionales, sin moverte de casa en', 'Our goal is to give you the peace of mind of being in professional hands, without leaving home in'),
    # FAQ section
    ('Preguntas Frecuentes -', 'Frequently Asked Questions -'),
    ('Resolvemos tus dudas sobre nuestro servicio de mecánico a domicilio en', 'We answer your questions about our mobile mechanic service in'),
    ('¿Buscas un mecánico a domicilio en', 'Looking for a mobile mechanic in'),
    ('En Global Pro Automotriz, somos la respuesta inmediata. No importa si estás en tu hogar, oficina o varado en la calle de', 'At GlobalPro Automotive, we are the immediate answer. Whether you are at home, at the office, or stranded on the street in'),
    ('nuestro servicio de mecánico a domicilio cubre toda la Región Metropolitana con rapidez y profesionalismo. Llevamos el taller mecánico a tu ubicación para que no pierdas tiempo ni dinero en grúas.',
     'our mobile mechanic service covers the entire Metropolitan Region with speed and professionalism. We bring the auto repair shop to your location so you don\'t waste time or money on tow trucks.'),
    ('¿Cuánto demoran en llegar a', 'How long does it take to get to'),
    ('En la mayoría de los casos atendemos en', 'In most cases, we serve you in'),
    ('en menos de 24 horas. Nuestro servicio de emergencia 24/7 puede llegar incluso el mismo día. La rapidez depende de la disponibilidad de nuestros técnicos y la urgencia del caso.',
     'within 24 hours. Our 24/7 emergency service can arrive the same day. Response time depends on technician availability and the urgency of the case.'),
    ('¿Qué servicios de mecánica ofrecen en', 'What mechanic services do you offer in'),
    ('Ofrecemos mecánica general, reparación de frenos, embrague, suspensión, electricidad automotriz, aire acondicionado, scanner diagnóstico, cambio de aceite, mantenimiento preventivo y correctivo, todo directamente en tu domicilio en',
     'We offer general mechanics, brake repair, clutch, suspension, auto electrical, air conditioning, diagnostic scanner, oil change, preventive and corrective maintenance, all at your doorstep in'),
    ('¿Cuánto cuesta el mecánico a domicilio en', 'How much does a mobile mechanic cost in'),
    ('El costo depende del servicio solicitado. Cotiza sin compromiso por WhatsApp y recibirás un presupuesto transparente sin sorpresas. No cobramos anticipos; solo pagas una vez finalizado el servicio en',
     'The cost depends on the service requested. Get a no-obligation quote via WhatsApp and receive a transparent estimate with no surprises. We don\'t charge upfront; you only pay once the service is completed in'),
    ('¿Tienen especialistas en mecánica de electricidad y alarmas en', 'Do you have electrical and alarm specialists in'),
    ('Absolutamente. Contamos con un eléctrico automotriz a domicilio experto en mecánica de electricidad, diagnóstico de alternadores y motores de partida. Además, realizamos la instalación y reparación de alarmas automotriz y sistemas de seguridad electrónica.',
     'Absolutely. We have a mobile auto electrician expert in electrical mechanics, alternator and starter motor diagnosis. We also perform installation and repair of car alarms and electronic security systems.'),
    ('¿Hacen reparaciones de aire acondicionado en', 'Do you do air conditioning repairs in'),
    ('Ofrecemos un servicio técnico integral que incluye la recarga de aire acondicionado auto y reparación de climatización directamente en', 'We offer a comprehensive technical service that includes auto AC recharge and climate control repair right in'),
    ('También gestionamos soluciones para parabrisas y cristales.', 'We also handle windshield and glass solutions.'),
    ('¿Puedo solicitar un cambio de aceite a domicilio en', 'Can I request an oil change at home in'),
    ('¡Claro que sí! Realizamos el cambio de aceite y filtro directamente en tu domicilio en', 'Of course! We perform oil and filter changes right at your home in'),
    ('utilizando insumos de alta calidad. Es parte de nuestro compromiso de mantenimiento automotriz preventivo.',
     'using high-quality supplies. It is part of our commitment to preventive automotive maintenance.'),
    ('¿Qué tipos de vehículos atienden en', 'What types of vehicles do you service in'),
    ('Atendemos autos, camionetas, SUVs y vehículos comerciales livianos de todas las marcas y modelos en', 'We service cars, pickup trucks, SUVs, and light commercial vehicles of all makes and models in'),
    ('¿Debo pagar por adelantado en', 'Do I have to pay upfront in'),
    ('No. Solo pagas una vez realizado el servicio. No cobramos anticipos ni sorpresas en el precio.',
     'No. You only pay once the service is done. We don\'t charge upfront and there are no surprises in the price.'),
    ('¿El diagnóstico incluye scanner en', 'Does the diagnosis include a scanner in'),
    ('Sí, si el tipo de falla lo requiere, se incluye sin costo adicional. Nuestros técnicos cuentan con scanner automotriz profesional para diagnóstico computarizado.',
     'Yes, if the type of fault requires it, it is included at no additional cost. Our technicians have professional automotive scanners for computerized diagnostics.'),
    # Maintenance section
    ('Mantención por Kilometraje en', 'Mileage-Based Maintenance in'),
    ('Revisamos todos los puntos indicados en la pauta de mantención de su vehículo según su kilometraje, directamente en', 'We check all the points indicated in your vehicle\'s maintenance schedule according to its mileage, right in'),
    ('Cambio de Filtro y Aceite', 'Oil and Filter Change'),
    ('Cambio de Filtro de Aire', 'Air Filter Change'),
    ('Revisión de Correas', 'Belt Inspection'),
    ('Cambio de Filtro de Polen', 'Pollen Filter Change'),
    ('Revisión de Frenos', 'Brake Inspection'),
    ('Revisión de Luces', 'Light Inspection'),
    ('Revisión de fluidos', 'Fluid Inspection'),
    ('Rotación de Neumáticos', 'Tire Rotation'),
    ('Scanner Automotriz', 'Automotive Scanner'),
    ('Asesoramos en Aceite y Filtros', 'Oil and Filter Advice'),
    ('Cotizar Mantención en', 'Get a Maintenance Quote in'),
    # Guarantees section
    ('Nuestras Garantías Profesionales', 'Our Professional Guarantees'),
    ('con experiencia comprobada', 'with proven experience'),
    ('Repuestos de calidad garantizada', 'Guaranteed quality parts'),
    ('Presupuesto claro sin costo', 'Clear estimate at no cost'),
    ('Garantia en todos los trabajos', 'Warranty on all jobs'),
    # Footer
    ('Enlaces Rápidos', 'Quick Links'),
    ('Sobre Nosotros', 'About Us'),
    ('Política de Privacidad', 'Privacy Policy'),
    ('Información de Contacto', 'Contact Information'),
    ('Síguenos', 'Follow Us'),
    ('Todos los derechos reservados', 'All rights reserved'),
    ('GlobalPro Automotriz', 'GlobalPro Automotive'),
    # Bottom bar
    ('LLAMAR AHORA', 'CALL NOW'),
    ('WHATSAPP', 'WHATSAPP'),
    # Pre-purchase inspection
    ('Inspección Pre-Compra', 'Pre-Purchase Inspection'),
    # Common Spanish words in text content
    ('En GlobalPro,', 'At GlobalPro,'),
    ('somos expertos en mecánica automotriz, electromecánica y mantenimiento.', 'we are experts in automotive mechanics, electromechanical systems, and maintenance.'),
    ('Servicio a domicilio en', 'Mobile service in'),
    ('y toda la Región Metropolitana.', 'and the entire Metropolitan Region.'),
    ('¡Tu vehículo en las mejores manos!', 'Your vehicle in the best hands!'),
    # Modals
    ('PERFIL EN GOOGLE', 'GOOGLE PROFILE'),
    ('MECANICO A DOMICILIO 24/7', 'MOBILE MECHANIC 24/7'),
    ('GLOBAL PRO Automotive', 'GLOBALPRO Automotive'),
    ('Escríbenos al WhatsApp y', 'Message us on WhatsApp and'),
    ('de forma rápida y sin compromiso', 'quickly and with no obligation'),
    ('ABIERTO', 'OPEN'),
    ('Las 24 horas', '24 Hours'),
    ('Services Principales', 'Main Services'),
    ('Mecanico a Domicilio', 'Mobile Mechanic'),
    ('cotiza tu servicio', 'get a service quote'),
    ('atencion personalizada', 'personalized attention'),
    ('sin costos ocultos ni sorpresas', 'with no hidden costs or surprises'),
    ('Agenda por WhatsApp y recibe', 'Schedule on WhatsApp and receive'),
    ('Orden Express', 'Express Order'),
    ('Busca por Patente', 'Search by License Plate'),
    ('BUSCAR', 'SEARCH'),
    ('Historial de Ordenes', 'Order History'),
    ('completo de trabajos, notas del técnico, fechas y más.', 'complete work details, technician notes, dates, and more.'),
    ('Sin Ordenes', 'No Orders'),
    ('Cotizar Calefaccion Ahora', 'Get a Heating Quote Now'),
    # Language switcher
    ('ES', 'ES'),
    # Alt tags
    ('alt="Mecánico a domicilio en', 'alt="Mobile mechanic in'),
    ('alt="Calefaccion y climatizacion automotriz en', 'alt="Automotive climate control and heating in'),
    # Pre-purchase section
    ('Inspección Pre-Compra', 'Pre-Purchase Inspection'),
    ('Nuestros expertos evalúan el estado real del vehículo antes de tu compra en', 'Our experts evaluate the real condition of the vehicle before your purchase in'),
    ('Evita sorpresas y decide con información completa.', 'Avoid surprises and make an informed decision.'),
]

# ============================================================================
# ADDITIONAL SPANISH → ENGLISH for general text found across all pages
# ============================================================================
GENERAL_REPLACEMENTS = [
    # Common phrases
    ('En GlobalPro Automotriz', 'At GlobalPro Automotive'),
    ('En GlobalPro', 'At GlobalPro'),
    ('nuestro equipo de técnicos certificados', 'our team of certified technicians'),
    ('se desplaza directamente a tu hogar, oficina o ubicación en', 'comes directly to your home, office, or location in'),
    ('llevando herramientas de diagnóstico de última generación y repuestos de calidad para resolver cualquier problema mecánico sin que tengas que moverte.',
     'bringing state-of-the-art diagnostic tools and quality replacement parts to solve any mechanical problem without you having to move.'),
    ('Ya sea que necesites un', 'Whether you need an'),
    ('o un', 'or a'),
    ('en GlobalPro tenemos la experiencia y el compromiso para atenderte en', 'at GlobalPro we have the experience and commitment to serve you in'),
    ('con la misma calidad de un taller formal pero con la comodidad de estar en tu propia puerta.', 'with the same quality as a formal shop but with the convenience of being at your own doorstep.'),
    ('Nos enorgullece ser el servicio de', 'We are proud to be the'),
    ('más confiable de la Región Metropolitana, con más de 5.000 clientes satisfechos que nos recomiendan.',
     'service most trusted in the Metropolitan Region, with over 5,000 satisfied customers who recommend us.'),
    ('es una de las comunas donde mayor demanda tenemos, y por eso hemos optimizado nuestros tiempos de respuesta para que un técnico esté contigo en menos de lo que imaginas.',
     'is one of the areas with the highest demand, which is why we have optimized our response times so a technician can be with you faster than you think.'),
    ('Si tu auto no arranca, tienes una falla en el sistema eléctrico, o simplemente necesitas la',
     'If your car won\'t start, you have an electrical system failure, or simply need your'),
    ('mantención preventiva', 'preventive maintenance'),
    ('al día, nuestro', 'up to date, our'),
    ('es la solución. Contáctanos por WhatsApp y agenda tu cita hoy mismo.',
     'is the solution. Contact us on WhatsApp and schedule your appointment today.'),
    ('Buscando un', 'Looking for a'),
    ('? En', '? At'),
    ('entendemos que los residentes de', 'we understand that residents of'),
    ('necesitan soluciones rápidas y confiables para el mantenimiento de sus vehículos.',
     'need fast and reliable solutions for their vehicle maintenance.'),
    # Generic patterns
    ('mecánico a domicilio', 'mobile mechanic'),
    ('Mecánico a Domicilio', 'Mobile Mechanic'),
    ('mecánico mobile service', 'mobile mechanic'),
    ('mecánico mobile service', 'mobile mechanic'),
    ('taller mecánico', 'auto repair shop'),
    ('Taller Mecánico', 'Auto Repair Shop'),
    ('taller móvil', 'mobile workshop'),
    ('servicio a domicilio', 'mobile service'),
    ('Servicio a Domicilio', 'At-Home Service'),
    ('mantención preventiva', 'preventive maintenance'),
    ('Mantención Preventiva', 'Preventive Maintenance'),
    ('mantenimiento preventivo', 'preventive maintenance'),
    ('cambio de aceite', 'oil change'),
    ('Cambio de Aceite', 'Oil Change'),
    ('reparación de frenos', 'brake repair'),
    ('Reparación de Frenos', 'Brake Repair'),
    ('diagnóstico con scanner', 'diagnostic scan'),
    ('servicio de emergencia 24/7', '24/7 emergency service'),
    ('automotriz', 'automotive'),
    ('Automotriz', 'Automotive'),
    ('vehículo', 'vehicle'),
    ('Vehículo', 'Vehicle'),
    ('vehículos', 'vehicles'),
    ('Vehículos', 'Vehicles'),
    ('reparación', 'repair'),
    ('mantenimiento', 'maintenance'),
    ('Mantenimiento', 'Maintenance'),
    ('cotizar', 'get a quote'),
    ('Cotizar', 'Get Quote'),
    ('cotiza', 'quote'),
    ('presupuesto', 'estimate'),
    ('Presupuesto', 'Estimate'),
    ('garantía', 'warranty'),
    ('Garantía', 'Warranty'),
    ('Garantias', 'Guarantees'),
    ('emergencia', 'emergency'),
    ('Emergencia', 'Emergency'),
    ('emergencias', 'emergencies'),
    ('Emergencias', 'Emergencies'),
    ('técnico', 'technician'),
    ('Técnico', 'Technician'),
    ('técnicos', 'technicians'),
    ('Técnicos', 'Technicians'),
    ('mecánico', 'mechanic'),
    ('Mecánico', 'Mechanic'),
    ('mecánicos', 'mechanics'),
    ('repuestos', 'parts'),
    ('Repuestos', 'Parts'),
    ('diagnóstico', 'diagnosis'),
    ('Diagnóstico', 'Diagnosis'),
    ('diagnosticar', 'diagnose'),
    ('scanner', 'scanner'),
    ('Scanner', 'Scanner'),
    ('Escáner', 'Scanner'),
]


def apply_replacements(html_content, replacements):
    """Apply all replacements to HTML content."""
    result = html_content
    for old, new in replacements:
        result = result.replace(old, new)
    return result


def fix_comuna_nav_links(html_content, slug):
    """Fix navigation links to point to /en/ versions."""
    # Replace Spanish nav links with English versions
    result = html_content
    # Fix comuna dropdown links
    for comuna_slug in COMUNA_DATA.keys():
        result = result.replace(f'href="/comunas/{comuna_slug}"', f'href="/en/comunas/{comuna_slug}"')
    # Fix other nav links
    result = result.replace('href="/quienes-somos"', 'href="/en/about-us"')
    result = result.replace('href="/contacto"', 'href="/en/contacto"')
    result = result.replace('href="/blog/"', 'href="/en/blog/"')
    result = result.replace('href="/vehiculos/"', 'href="/en/vehiculos/"')
    result = result.replace('href="/faq"', 'href="/en/faq"')
    result = result.replace('href="/politica-privacidad"', 'href="/en/privacy-policy"')
    # Fix home link
    result = result.replace('href="/#mecanico-domicilio-seo"', 'href="/en/#mobile-mechanic-seo"')
    result = result.replace('href="/#servicios"', 'href="/en/#servicios"')
    # Fix logo link
    result = result.replace('href="/" class="logo', 'href="/en/" class="logo')
    return result


def fix_canonical_and_hreflang(html_content, slug, page_type='comunas'):
    """Fix canonical URL and hreflang tags for English pages."""
    result = html_content
    
    # Fix canonical
    result = result.replace(
        f'href="https://mecanico247.com/{page_type}/{slug}"',
        f'href="https://mecanico247.com/en/{page_type}/{slug}"'
    )
    
    # Fix hreflang - remove duplicates and set correct ones
    # Remove all existing hreflang lines
    result = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\s*\n?', '', result)
    
    # Add correct hreflang before </head>
    es_url = f'https://mecanico247.com/{page_type}/{slug}'
    en_url = f'https://mecanico247.com/en/{page_type}/{slug}'
    hreflang_tags = f'''<link rel="alternate" hreflang="es" href="{es_url}" />
<link rel="alternate" hreflang="en" href="{en_url}" />
<link rel="alternate" hreflang="x-default" href="{es_url}" />
'''
    result = result.replace('</head>', hreflang_tags + '</head>')
    
    return result


def fix_og_tags(html_content, slug, page_type='comunas'):
    """Fix Open Graph and Twitter tags."""
    result = html_content
    en_url = f'https://mecanico247.com/en/{page_type}/{slug}'
    result = result.replace(
        f'<meta property="og:url" content="https://mecanico247.com/{page_type}/{slug}"/>',
        f'<meta property="og:url" content="{en_url}"/>'
    )
    result = result.replace(
        f'<meta property="og:url" content="https://mecanico247.com/{page_type}/{slug}">',
        f'<meta property="og:url" content="{en_url}">'
    )
    result = result.replace('og:locale" content="es_CL"', 'og:locale" content="en_US"')
    result = result.replace('og:locale" content="es_ES"', 'og:locale" content="en_US"')
    result = result.replace('og:site_name" content="GlobalPro Automotriz"', 'og:site_name" content="GlobalPro Automotive"')
    return result


def add_language_switcher(html_content):
    """Add ES/EN language switcher if not present."""
    if 'lang-switch' in html_content or 'langSwitcher' in html_content:
        return html_content
    
    switcher_css = '''
<style>
.lang-switch {
  position: fixed;
  top: 15px;
  right: 80px;
  z-index: 10002;
  display: flex;
  gap: 4px;
  background: rgba(0,0,0,0.8);
  border-radius: 20px;
  padding: 4px;
  border: 1px solid rgba(255,255,255,0.2);
}
.lang-switch a {
  padding: 5px 12px;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 700;
  text-decoration: none;
  color: #ccc;
  transition: all 0.2s;
}
.lang-switch a.active {
  background: #a80000;
  color: #fff;
}
.lang-switch a:hover {
  color: #fff;
}
</style>
'''
    # Determine the Spanish equivalent URL
    switcher_html = '''
<div class="lang-switch">
  <a href="#" onclick="window.location.href=window.location.href.replace('/en/','/'); return false;">ES</a>
  <a href="#" class="active">EN</a>
</div>
'''
    # Insert CSS before </head>
    html_content = html_content.replace('</head>', switcher_css + '</head>')
    # Insert switcher after body tag
    html_content = html_content.replace('<body>', '<body>' + switcher_html)
    
    return html_content


def process_comuna_page(slug):
    """Read Spanish source, translate to English, save to /en/."""
    comuna = COMUNA_DATA[slug]
    name = comuna['name']
    zone = comuna['zone']
    
    es_path = f'comunas/{slug}.html'
    en_path = f'en/comunas/{slug}.html'
    
    if not os.path.exists(es_path):
        print(f"  SKIP: {es_path} not found")
        return False
    
    with open(es_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Apply all replacements
    result = apply_replacements(html_content, COMUNA_REPLACEMENTS)
    result = apply_replacements(result, GENERAL_REPLACEMENTS)
    
    # Fix navigation links
    result = fix_comuna_nav_links(result, slug)
    
    # Fix canonical and hreflang
    result = fix_canonical_and_hreflang(result, slug, 'comunas')
    
    # Fix OG tags
    result = fix_og_tags(result, slug, 'comunas')
    
    # Add language switcher
    result = add_language_switcher(result)
    
    # Fix title tags
    result = result.replace(
        f'Taller Mecánico en {name} | GlobalPro Automotriz',
        f'Mobile Mechanic in {name} | GlobalPro Automotive - Santiago'
    )
    result = result.replace(
        f'Mecánico a Domicilio en {name} | GlobalPro Automotriz',
        f'Mobile Mechanic in {name} | GlobalPro Automotive - Santiago'
    )
    
    # Fix meta description
    result = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="Mobile mechanic service in {name}, Santiago 24/7. Brake repair, clutch, electrical, diagnostics, air conditioning, preventive maintenance. 5,000+ customers served. Get a quote on WhatsApp."',
        result
    )
    
    # Fix WhatsApp links
    wa_text = f'Hi%20I%20need%20a%20mobile%20mechanic%20in%20{slug}'
    result = result.replace(
        f'Hola%20necesito%20un%20mecanico%20a%20domicilio%20en%20{slug}',
        wa_text
    )
    result = result.replace(
        f'Hola%20necesito%20un%20mecanico%20a%20domicilio%20en%20maipu',
        wa_text
    )
    # Generic WA text replacements
    result = result.replace('Hola%20necesito%20un%20mecanico%20a%20domicilio%20en%20', 'Hi%20I%20need%20a%20mobile%20mechanic%20in%20')
    result = result.replace('Hola,%20quiero%20cotizar%20por%20', 'Hi,%20I%20want%20a%20quote%20for%20')
    result = result.replace('Hola%20necesito%20reparacion%20de%20frenos%20a%20domicilio%20en%20', 'Hi%20I%20need%20brake%20repair%20at%20home%20in%20')
    result = result.replace('Hola%20necesito%20electricidad%20automotriz%20a%20domicilio%20en%20', 'Hi%20I%20need%20auto%20electrical%20service%20at%20home%20in%20')
    result = result.replace('Hola%20necesito%20scanner%20automotriz%20a%20domicilio%20en%20', 'Hi%20I%20need%20a%20diagnostic%20scan%20at%20home%20in%20')
    result = result.replace('Hola%20necesito%20un%20cambio%20de%20aceite%20a%20domicilio%20en%20', 'Hi%20I%20need%20an%20oil%20change%20at%20home%20in%20')
    result = result.replace('Hola%20necesito%20servicio%20de%20calefaccion%20automotriz%20en%20', 'Hi%20I%20need%20automotive%20heating%20service%20in%20')
    
    # Fix logo subtitle
    result = result.replace('Taller Mecánico', 'Auto Repair Shop')
    
    # Fix structured data
    result = result.replace('"GlobalPro Automotriz"', '"GlobalPro Automotive"')
    result = result.replace('"GlobalPro Auto Repair"', '"GlobalPro Automotive"')
    result = result.replace('addressRegion": "Región Metropolitana"', 'addressRegion": "Metropolitan Region"')
    
    # Fix breadcrumb
    result = result.replace('"name": "Home"\n      "item": "https://mecanico247.com/"', '"name": "Home"\n      "item": "https://mecanico247.com/en/"')
    result = result.replace('"name": "Comunas"', '"name": "Areas"')
    result = result.replace('"item": "https://mecanico247.com/comunas/"', '"item": "https://mecanico247.com/en/comunas/"')
    result = result.replace(f'"item": "https://mecanico247.com/comunas/{slug}"', f'"item": "https://mecanico247.com/en/comunas/{slug}"')
    
    # Fix calefacción section for English
    result = fix_calefaccion_section(result, name)
    
    # Fix detailed services section - translate the specific comuna text
    result = fix_detailed_services(result, name, zone)
    
    # Fix FAQ structured data
    result = fix_faq_schema(result, name, slug)
    
    # Ensure proper lang attribute
    result = result.replace('lang="es"', 'lang="en"')
    
    # Fix remaining "en" vs "in" - the Spanish word "en" should be "in" in English
    # But be careful - "en" appears in many English words too
    # Only fix standalone "en " at word boundaries in text content
    
    # Write the result
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  OK: {en_path}")
    return True


def fix_calefaccion_section(html_content, comuna_name):
    """Translate the calefacción/heating section to proper English."""
    result = html_content
    
    # Replace the entire heating section content with proper English
    # Find the section by its ID
    if 'calefaccion-automotriz' not in result:
        return result
    
    # Replace Spanish text in the heating section
    heating_replacements = [
        ('Si tu sistema esta fallando o necesitas mejorar el confort de tu viaje en Santiago, nuestro equipo tecnico cuenta con unidades de respuesta rapida. Nos especializamos en el diagnostico, reparacion e instalacion de',
         'If your system is failing or you need to improve your travel comfort in Santiago, our technical team has rapid response units. We specialize in the diagnosis, repair, and installation of'),
        ('calefaccion para vehiculos', 'vehicle heating'),
        ('calefaccion para autos', 'car heating'),
        ('calefaccion para furgoneta', 'van heating'),
        ('directamente en tu ubicacion', 'directly at your location'),
        ('Cuando las bajas temperaturas se hacen sentir, garantizamos que la calefaccion en el coche o la calefaccion de coche funcione a su maxima capacidad y con total seguridad.',
         'When low temperatures hit, we ensure your car heating system works at full capacity with complete safety.'),
        ('Sabemos que cada tipo de transporte requiere una solucion tecnica diferente. Por eso, nuestros tecnicos capacitados manejan a la perfeccion desde sistemas tradicionales de',
         'We know that each type of vehicle requires a different technical solution. That is why our trained technicians handle everything from traditional'),
        ('calefaccion coche', 'car heating'),
        ('hasta tecnologias especificas como la', 'to specific technologies such as'),
        ('calefaccion estacionaria coche', 'stationary car heating'),
        ('calefaccion estacionaria para camiones', 'stationary truck heating'),
        ('calefaccion para camion', 'truck heating'),
        ('Ademas, si eres amante de los viajes y la vida en ruta, resolvemos cualquier problema de',
         'Additionally, if you love road trips and van life, we solve any problem with'),
        ('calefaccion furgoneta', 'van heating'),
        ('calefaccion furgoneta 12v', '12v van heating'),
        ('calefaccion portatil furgoneta', 'portable van heating'),
        ('garantizando el clima ideal mediante sistemas especializados como la',
         'ensuring the ideal climate through specialized systems such as'),
        ('calefaccion diesel motorhome', 'diesel motorhome heating'),
        ('calefaccion estacionaria caravana', 'stationary caravan heating'),
        ('calefaccion para autocaravana', 'motorhome heating'),
        ('calefaccion para casa rodante', 'RV heating'),
        ('Para quienes camperizan sus vehiculos, entregamos soluciones eficientes en',
         'For those who convert their vehicles into campers, we deliver efficient solutions in'),
        ('calefaccion de vehiculos', 'vehicle heating'),
        ('calefaccion estatica furgoneta', 'static van heating'),
        ('calefaccion para furgonetas camper', 'camper van heating'),
        ('calefaccion electrica furgoneta', 'electric van heating'),
        ('Atendemos fallas complejas de eficiencia energetica, evaluando si la calefaccion coche consume gasolina en exceso o si es mejor implementar alternativas modernas como la',
         'We handle complex energy efficiency issues, evaluating whether the car heating system consumes excessive gasoline or if it is better to implement modern alternatives such as'),
        ('calefaccion electrica para automoviles', 'electric car heating'),
        ('calefaccion electrica para coche', 'electric car heater'),
        ('calefaccion auxiliar para coche', 'auxiliary car heater'),
        ('Asimismo, optimizamos sistemas pesados configurando',
         'Likewise, we optimize heavy-duty systems by configuring'),
        ('calefaccion auxiliar para furgonetas', 'auxiliary van heater'),
        ('calefaccion autonoma coche', 'autonomous car heater'),
        ('para un rendimiento continuo', 'for continuous performance'),
        ('El confort termico interior tambien abarca los componentes electricos directos. Resolvemos desperfectos en la',
         'Interior thermal comfort also covers direct electrical components. We fix issues with'),
        ('calefaccion asiento coche', 'heated car seats'),
        ('calefaccion en asientos coche', 'car seat heating'),
        ('y en la distribucion de energia como la', 'and in power distribution such as'),
        ('calefaccion bateria coche', 'car battery heating'),
        ('Nuestros mecanicos cuentan con el equipamiento para sustituir componentes especificos del habitaculo, incluyendo fallas comunes de climatizacion multimarca como la',
         'Our mechanics have the equipment to replace specific interior components, including common multi-brand climate control issues such as'),
        ('resistencia calefaccion peugeot 207', 'Peugeot 207 heater resistor'),
        ('No arriesgues la comodidad de tus pasajeros; si buscas optimizar la',
         "Don't risk your passengers' comfort; if you want to optimize"),
        ('calefaccion de autos', 'car heating'),
        ('calefaccion autos', 'car heating'),
        ('calefaccion carro', 'vehicle heating'),
        ('calefaccion vehiculos', 'vehicle heating'),
        ('o requieres una', 'or you need a'),
        ('calefaccion para coche', 'car heater'),
        ('tradicional o una', 'or a'),
        ('calefaccion para autos portatil', 'portable car heater'),
        ('activa tu Orden Express ahora', 'activate your Express Order now'),
        ('Cotizar Calefaccion Ahora', 'Get a Heating Quote Now'),
        ('Servicio Avanzado de Climatizacion y Calefaccion Automotriz 24/7 en',
         'Advanced Automotive Climate Control and Heating Service 24/7 in'),
        ('alt="Calefaccion y climatizacion automotriz en', 'alt="Automotive climate control and heating in'),
    ]
    
    for old, new in heating_replacements:
        result = result.replace(old, new)
    
    return result


def fix_detailed_services(html_content, comuna_name, zone):
    """Fix the detailed service blocks that have comuna-specific text."""
    result = html_content
    
    # Translate the 10 detailed service blocks
    # These contain comuna-specific text that needs careful translation
    
    # Block 1: Mobile Mechanic
    result = result.replace(
        'GlobalPro Automotriz lleva el taller mecanico hasta la puerta de tu hogar en',
        'GlobalPro Automotive brings the auto repair shop to your doorstep in'
    )
    result = result.replace(
        'No tienes que perder tiempo en traslados ni esperas en talleres: nuestros tecnicos certificados llegan con herramientas de diagnostico profesional y repuestos de calidad para atender sedan compactos, SUV y vehiculos familiares directamente en tu domicilio.',
        'No need to waste time on trips or waiting at shops: our certified technicians arrive with professional diagnostic tools and quality parts to service compact sedans, SUVs, and family vehicles right at your home.'
    )
    result = result.replace(
        'Conectamos con los barrios de',
        'We connect with the neighborhoods of'
    )
    result = result.replace(
        'para ofrecerte un servicio rapido y confiable, sin costos ocultos ni sorpresas. Agenda por WhatsApp y recibe atencion personalizada.',
        'to offer you a fast and reliable service, with no hidden costs or surprises. Schedule on WhatsApp and receive personalized attention.'
    )
    
    # Block 2: Scanner
    result = result.replace(
        'El scanner automotriz es la herramienta clave para un diagnostico preciso sin adivinanzas.',
        'The automotive scanner is the key tool for an accurate diagnosis with no guesswork.'
    )
    result = result.replace(
        'En GlobalPro, realizamos escaneos electronicos completos en',
        'At GlobalPro, we perform complete electronic scans in'
    )
    result = result.replace(
        'para detectar fallas en sensores, modulos ECU, sistemas de inyeccion, ABS, airbag y mas.',
        'to detect faults in sensors, ECU modules, injection systems, ABS, airbags, and more.'
    )
    result = result.replace(
        'Los vehiculos que circulan por poniente de Santiago enfrentan condiciones de trafico y clima que generan codigos de error especificos.',
        'Vehicles driving through the metropolitan area face traffic and weather conditions that generate specific error codes.'
    )
    result = result.replace(
        'Nuestros tecnicos interpretan cada codigo y ofrecen soluciones reales para que tu auto vuelva a funcionar como nuevo a domicilio.',
        'Our technicians interpret each code and offer real solutions so your car runs like new again, right at your doorstep.'
    )
    
    # Block 3: Brakes
    result = result.replace(
        'La seguridad de tu familia depende del estado de los frenos.',
        'Your family\'s safety depends on the condition of your brakes.'
    )
    result = result.replace(
        'En GlobalPro revisamos pastillas, discos, calipers, latiguillos y fluido hidraulico directamente en',
        'At GlobalPro we inspect pads, rotors, calipers, brake lines, and hydraulic fluid right in'
    )
    result = result.replace(
        'El trafico frecuente por Autopista del Sol, Vespucio Oeste y metro acelera el desgaste de los componentes de frenado.',
        'Frequent traffic on highways and main roads accelerates the wear of braking components.'
    )
    result = result.replace(
        'Nuestro servicio incluye medicion digital del espesor de pastillas, diagnostico de vibraciones en frenada y reemplazo con componentes de alta especificacion. No arriesgues: agenda tu revision de frenos a domicilio en',
        'Our service includes digital measurement of pad thickness, diagnosis of braking vibrations, and replacement with high-specification components. Don\'t take risks: schedule your brake inspection at home in'
    )
    
    # Block 4: Oil Change
    result = result.replace(
        'El cambio de aceite periodico es la inversion mas importante para proteger el motor de tu vehiculo.',
        'Regular oil changes are the most important investment to protect your vehicle\'s engine.'
    )
    result = result.replace(
        'GlobalPro realiza este servicio a domicilio en',
        'GlobalPro performs this service at your home in'
    )
    result = result.replace(
        'con aceites sinteticos y semi-sinteticos premium de marcas como Castrol, Mobil y Shell.',
        'with premium synthetic and semi-synthetic oils from brands like Castrol, Mobil, and Shell.'
    )
    result = result.replace(
        'Incluimos filtro de aceite, revision del filtro de aire y checkeo de liquidos.',
        'We include oil filter, air filter inspection, and fluid level check.'
    )
    result = result.replace(
        'Para los sedan compactos, SUV y vehiculos familiares que circulan por poniente de Santiago, las condiciones de uso urbano requieren intervalos de cambio de entre 5.000 y 10.000 km. Agenda rapido por WhatsApp.',
        'For compact sedans, SUVs, and family vehicles driving in the metropolitan area, urban driving conditions require change intervals between 5,000 and 10,000 km. Schedule quickly on WhatsApp.'
    )
    
    # Block 5: Alignment and Suspension
    result = result.replace(
        'Las calles y avenidas de',
        'The streets and avenues of'
    )
    result = result.replace(
        'pueden afectar la alineacion y suspension de tu vehiculo.',
        'can affect your vehicle\'s alignment and suspension.'
    )
    result = result.replace(
        'Baches, badenes y resaltos generan desgaste en amortiguadores, rotulas, terminales y bujes.',
        'Potholes, speed bumps, and uneven surfaces cause wear on shock absorbers, ball joints, tie rods, and bushings.'
    )
    result = result.replace(
        'GlobalPro realiza alineacion computarizada y revision completa de suspension a domicilio en',
        'GlobalPro performs computerized alignment and complete suspension inspection at your home in'
    )
    result = result.replace(
        'Detectamos vibraciones en el volante, desgaste irregular de neumaticos y desalineacion con equipos de precision, devolviendo estabilidad y seguridad a tu vehiculo sin que salgas de casa.',
        'We detect steering wheel vibrations, irregular tire wear, and misalignment with precision equipment, restoring stability and safety to your vehicle without you leaving home.'
    )
    
    # Block 6: Engine Repair
    result = result.replace(
        'Cuando tu vehiculo presenta perdida de potencia, consumo excesivo de aceite, humo en el escape o ruidos anormales, puede que necesites una revision del motor a fondo.',
        'When your vehicle shows power loss, excessive oil consumption, exhaust smoke, or abnormal noises, you may need a thorough engine inspection.'
    )
    result = result.replace(
        'En GlobalPro, atendemos sedan compactos, SUV y vehiculos familiares en',
        'At GlobalPro, we service compact sedans, SUVs, and family vehicles in'
    )
    result = result.replace(
        'con diagnostico avanzado que incluye prueba de compresion y pre-compresion para evaluar el estado interno de cilindros, pistones y anillos.',
        'with advanced diagnostics including compression and leak-down tests to evaluate the internal condition of cylinders, pistons, and rings.'
    )
    result = result.replace(
        'Nuestros mecanicos resuelven desde fallas menores por alto kilometraje como juntas de tapa de valvulas hasta reparaciones mayores del bloque.',
        'Our mechanics resolve everything from minor high-mileage issues like valve cover gaskets to major block repairs.'
    )
    
    # Block 7: Clutch and Timing Belt
    result = result.replace(
        'El embrague y la correa de distribucion son componentes criticos que no pueden fallar.',
        'The clutch and timing belt are critical components that cannot fail.'
    )
    result = result.replace(
        'Un embrague desgastado dificulta los cambios de marcha, mientras que una correa rota puede danar irreversiblemente el motor.',
        'A worn clutch makes gear shifting difficult, while a broken belt can irreversibly damage the engine.'
    )
    result = result.replace(
        'GlobalPro atiende emergencias mecanicas en',
        'GlobalPro handles mechanical emergencies in'
    )
    result = result.replace(
        'para reemplazar estos componentes con kits completos de calidad OEM.',
        'to replace these components with complete OEM-quality kits.'
    )
    result = result.replace(
        'Atendemos sedan compactos, SUV y vehiculos familiares con repuestos certificados, garantizando un trabajo profesional sin tener que remolcar tu vehiculo a un taller.',
        'We service compact sedans, SUVs, and family vehicles with certified parts, guaranteeing professional work without having to tow your vehicle to a shop.'
    )
    
    # Block 8: Battery and Electrical
    result = result.replace(
        'Si tu vehiculo no arranca, las luces se ven debiles o escuchas click al girar la llave, el problema puede ser la bateria o el sistema electrico.',
        'If your vehicle won\'t start, lights look dim, or you hear a click when turning the key, the problem could be the battery or electrical system.'
    )
    result = result.replace(
        'En GlobalPro realizamos diagnostico de electricidad automotriz completo a domicilio en',
        'At GlobalPro we perform complete auto electrical diagnosis at your home in'
    )
    result = result.replace(
        'medimos carga de bateria, probamos el alternador, verificamos el motor de arranque y revisamos cableado.',
        'we measure battery charge, test the alternator, verify the starter motor, and inspect wiring.'
    )
    result = result.replace(
        'Los cambios de temperatura en poniente de Santiago afectan directamente la vida util de la bateria. Respondemos emergencias 24/7 para que no te quedes varado.',
         'Temperature changes in the metropolitan area directly affect battery life. We respond to 24/7 emergencies so you don\'t get stranded.'
    )
    
    # Block 9: Spark Plugs
    result = result.replace(
        'Las bujias desgastadas aumentan el consumo de combustible y reducen la potencia de tu vehiculo.',
        'Worn spark plugs increase fuel consumption and reduce your vehicle\'s power.'
    )
    result = result.replace(
        'En GlobalPro, reemplazamos bujias con las especificaciones exactas del fabricante a domicilio en',
        'At GlobalPro, we replace spark plugs to the manufacturer\'s exact specifications at your home in'
    )
    result = result.replace(
        'Complementamos con un plan de mantencion a domicilio y preventiva que incluye revision de filtros, aceites, liquido de frenos, anticongelante y correas.',
        'We complement this with an at-home preventive maintenance plan that includes filter, oil, brake fluid, coolant, and belt inspection.'
    )
    result = result.replace(
        'Un vehiculo bien mantenido dura mas anos y evita reparaciones costosas. Agenda tu mantencion preventiva en',
        'A well-maintained vehicle lasts longer and avoids costly repairs. Schedule your preventive maintenance in'
    )
    
    # Block 10: Emergencies
    result = result.replace(
        'Si tu vehiculo se queda varado en',
        'If your vehicle breaks down in'
    )
    result = result.replace(
        'o sufres una emergencia mecanica en poniente de Santiago, GlobalPro responde las 24 horas del dia.',
        'or you suffer a mechanical emergency in the metropolitan area, GlobalPro responds 24 hours a day.'
    )
    result = result.replace(
        'Somos el taller mecanico a domicilio mas cercano a ti, tu taller mecanico cerca de mi: llegamos en menos de 60 minutos para emergencias.',
        'We are the nearest mobile auto repair shop to you: we arrive in under 60 minutes for emergencies.'
    )
    result = result.replace(
        'Desde baterias descargadas hasta fallas de motor, nuestros tecnicos ofrecen soluciones inmediatas en',
        'From dead batteries to engine failures, our technicians offer immediate solutions in'
    )
    result = result.replace(
        'y alrededores. No importa la hora ni el lugar: GlobalPro es tu mecanico de confianza en',
        'and surrounding areas. No matter the time or place: GlobalPro is your trusted mechanic in'
    )
    result = result.replace(
        'para cualquier emergencia automotriz.',
        'for any automotive emergency.'
    )
    
    return result


def fix_faq_schema(html_content, comuna_name, slug):
    """Fix FAQ structured data to English."""
    result = html_content
    
    # Fix FAQ schema questions and answers
    faq_fixes = {
        f'¿Buscas un mecánico a domicilio en {comuna_name}?': f'Looking for a mobile mechanic in {comuna_name}?',
        f'En Global Pro Automotriz, somos la respuesta inmediata.': f'At GlobalPro Automotive, we are the immediate answer.',
        f'¿Cuánto demoran en llegar a {comuna_name}?': f'How long does it take to get to {comuna_name}?',
        f'¿Qué servicios de mecánica ofrecen en {comuna_name}?': f'What mechanic services do you offer in {comuna_name}?',
        f'¿Cuánto cuesta el mecánico a domicilio en {comuna_name}?': f'How much does a mobile mechanic cost in {comuna_name}?',
        f'¿Tienen especialistas en mecánica de electricidad y alarmas en {comuna_name}?': f'Do you have electrical and alarm specialists in {comuna_name}?',
        f'¿Hacen reparaciones de aire acondicionado en {comuna_name}?': f'Do you do air conditioning repairs in {comuna_name}?',
        f'¿Puedo solicitar un cambio de aceite a domicilio en {comuna_name}?': f'Can I request an oil change at home in {comuna_name}?',
        f'¿Qué tipos de vehículos atienden en {comuna_name}?': f'What types of vehicles do you service in {comuna_name}?',
        f'¿Debo pagar por adelantado en {comuna_name}?': f'Do I have to pay upfront in {comuna_name}?',
        f'¿El diagnóstico incluye scanner en {comuna_name}?': f'Does the diagnosis include a scanner in {comuna_name}?',
    }
    
    for old, new in faq_fixes.items():
        result = result.replace(old, new)
    
    return result


def process_vehiculo_page(slug):
    """Process a vehicle page."""
    data = VEHICULO_DATA.get(slug)
    if not data:
        print(f"  SKIP: No data for {slug}")
        return False
    
    name = data['name']
    vtype = data['type']
    brand = data['brand']
    
    es_path = f'vehiculos/{slug}.html'
    en_path = f'en/vehiculos/{slug}.html'
    
    if not os.path.exists(es_path):
        print(f"  SKIP: {es_path} not found")
        return False
    
    with open(es_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Apply general replacements first
    result = apply_replacements(html_content, GENERAL_REPLACEMENTS)
    
    # Vehicle-specific replacements
    result = result.replace('lang="es"', 'lang="en"')
    result = result.replace('Taller Mecánico', 'Auto Repair Shop')
    result = result.replace('Mecánico a Domicilio', 'Mobile Mechanic')
    result = result.replace('mecánico a domicilio', 'mobile mechanic')
    result = result.replace('Servicios', 'Services')
    result = result.replace('Comunas', 'Areas')
    result = result.replace('Quiénes Somos', 'About Us')
    result = result.replace('Contacto', 'Contact')
    result = result.replace('Vehiculos', 'Vehicles')
    result = result.replace('Privacidad', 'Privacy')
    
    # Fix nav links
    result = fix_comuna_nav_links(result, slug)
    # Fix vehicle nav links
    for vslug in VEHICULO_DATA.keys():
        result = result.replace(f'href="/vehiculos/{vslug}"', f'href="/en/vehiculos/{vslug}"')
    
    # Fix canonical and hreflang
    result = fix_canonical_and_hreflang(result, slug, 'vehiculos')
    result = fix_og_tags(result, slug, 'vehiculos')
    
    # Add language switcher
    result = add_language_switcher(result)
    
    # Fix WhatsApp links
    result = result.replace('Hola%20necesito%20', 'Hi%20I%20need%20')
    result = result.replace('Hola,%20quiero%20cotizar%20por%20', 'Hi,%20I%20want%20a%20quote%20for%20')
    
    # Fix title
    result = result.replace('GlobalPro Automotriz', 'GlobalPro Automotive')
    
    # Fix logo
    result = result.replace('href="/" class="logo', 'href="/en/" class="logo')
    
    # Write
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  OK: {en_path}")
    return True


def process_servicio_page(slug):
    """Process a service page."""
    data = SERVICIO_DATA.get(slug)
    if not data:
        print(f"  SKIP: No data for {slug}")
        return False
    
    name = data['name']
    es_name = data['es_name']
    
    es_path = f'servicios/{es_name}.html'
    en_path = f'en/servicios/{slug}.html'
    
    if not os.path.exists(es_path):
        print(f"  SKIP: {es_path} not found")
        return False
    
    with open(es_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Apply general replacements
    result = apply_replacements(html_content, GENERAL_REPLACEMENTS)
    
    # Service-specific replacements
    result = result.replace('lang="es"', 'lang="en"')
    result = result.replace('Taller Mecánico', 'Auto Repair Shop')
    result = result.replace('Mecánico a Domicilio', 'Mobile Mechanic')
    result = result.replace('Servicios', 'Services')
    result = result.replace('Comunas', 'Areas')
    result = result.replace('Quiénes Somos', 'About Us')
    result = result.replace('Contacto', 'Contact')
    result = result.replace('Vehiculos', 'Vehicles')
    result = result.replace('Privacidad', 'Privacy')
    result = result.replace('Cotizar Ahora', 'Get a Quote')
    result = result.replace('Cotizar', 'Get Quote')
    
    # Fix nav links
    result = fix_comuna_nav_links(result, slug)
    for sslug, sdata in SERVICIO_DATA.items():
        result = result.replace(f'href="/servicios/{sdata["es_name"]}"', f'href="/en/servicios/{sslug}"')
    
    # Fix canonical
    result = fix_canonical_and_hreflang(result, slug, 'servicios')
    result = fix_og_tags(result, slug, 'servicios')
    
    # Add language switcher
    result = add_language_switcher(result)
    
    # Fix WhatsApp
    result = result.replace('Hola%20necesito%20', 'Hi%20I%20need%20')
    result = result.replace('Hola,%20quiero%20cotizar%20por%20', 'Hi,%20I%20want%20a%20quote%20for%20')
    
    # Fix title and brand
    result = result.replace('GlobalPro Automotriz', 'GlobalPro Automotive')
    result = result.replace('href="/" class="logo', 'href="/en/" class="logo')
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  OK: {en_path}")
    return True


def process_marca_page(slug):
    """Process a brand page."""
    data = MARCA_DATA.get(slug)
    if not data:
        print(f"  SKIP: No data for {slug}")
        return False
    
    es_path = f'marcas_automotrices/{slug}.html'
    en_path = f'en/marcas_automotrices/{slug}.html'
    
    if not os.path.exists(es_path):
        print(f"  SKIP: {es_path} not found")
        return False
    
    with open(es_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    result = apply_replacements(html_content, GENERAL_REPLACEMENTS)
    result = result.replace('lang="es"', 'lang="en"')
    result = result.replace('Taller Mecánico', 'Auto Repair Shop')
    result = result.replace('Mecánico a Domicilio', 'Mobile Mechanic')
    result = result.replace('Servicios', 'Services')
    result = result.replace('Comunas', 'Areas')
    result = result.replace('Quiénes Somos', 'About Us')
    result = result.replace('Contacto', 'Contact')
    result = result.replace('Vehiculos', 'Vehicles')
    result = result.replace('Privacidad', 'Privacy')
    result = result.replace('Cotizar Ahora', 'Get a Quote')
    result = result.replace('Cotizar', 'Get Quote')
    result = result.replace('Marcas Automotrices', 'Automotive Brands')
    
    # Fix nav links
    result = fix_comuna_nav_links(result, slug)
    for mslug in MARCA_DATA.keys():
        result = result.replace(f'href="/marcas_automotrices/{mslug}"', f'href="/en/marcas_automotrices/{mslug}"')
    
    result = fix_canonical_and_hreflang(result, slug, 'marcas_automotrices')
    result = fix_og_tags(result, slug, 'marcas_automotrices')
    result = add_language_switcher(result)
    result = result.replace('Hola%20necesito%20', 'Hi%20I%20need%20')
    result = result.replace('Hola,%20quiero%20cotizar%20por%20', 'Hi,%20I%20want%20a%20quote%20for%20')
    result = result.replace('GlobalPro Automotriz', 'GlobalPro Automotive')
    result = result.replace('href="/" class="logo', 'href="/en/" class="logo')
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  OK: {en_path}")
    return True


def process_standalone_page(filename):
    """Process standalone pages like index.html, about-us.html, etc."""
    en_path = f'en/{filename}'
    
    # Map to Spanish source
    es_map = {
        'index.html': 'index.html',
        'about-us.html': 'quienes-somos.html',
        'contacto.html': 'contacto.html',
        'faq.html': 'faq.html',
        'privacy-policy.html': 'politica-privacidad.html',
        '404.html': '404.html',
        'mechanical-inspection.html': 'inspeccion-mecanica.html',
        'services-at-home.html': 'servicios-domicilio.html',
    }
    
    es_file = es_map.get(filename)
    if not es_file:
        print(f"  SKIP: No mapping for {filename}")
        return False
    
    if not os.path.exists(es_file):
        print(f"  SKIP: {es_file} not found")
        return False
    
    with open(es_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    result = apply_replacements(html_content, GENERAL_REPLACEMENTS)
    result = result.replace('lang="es"', 'lang="en"')
    result = result.replace('Taller Mecánico', 'Auto Repair Shop')
    result = result.replace('Mecánico a Domicilio', 'Mobile Mechanic')
    result = result.replace('Servicios', 'Services')
    result = result.replace('Comunas', 'Areas')
    result = result.replace('Quiénes Somos', 'About Us')
    result = result.replace('Contacto', 'Contact')
    result = result.replace('Vehiculos', 'Vehicles')
    result = result.replace('Privacidad', 'Privacy')
    result = result.replace('Cotizar Ahora', 'Get a Quote')
    result = result.replace('Cotizar', 'Get Quote')
    
    # Fix nav links
    result = fix_comuna_nav_links(result, '')
    
    # Fix specific page links
    result = result.replace('href="/quienes-somos"', 'href="/en/about-us"')
    result = result.replace('href="/contacto"', 'href="/en/contacto"')
    result = result.replace('href="/faq"', 'href="/en/faq"')
    result = result.replace('href="/politica-privacidad"', 'href="/en/privacy-policy"')
    result = result.replace('href="/inspeccion-mecanica"', 'href="/en/mechanical-inspection"')
    result = result.replace('href="/servicios-domicilio"', 'href="/en/services-at-home"')
    
    # Fix service links
    for sslug, sdata in SERVICIO_DATA.items():
        result = result.replace(f'href="/servicios/{sdata["es_name"]}"', f'href="/en/servicios/{sslug}"')
    
    # Fix vehicle links
    for vslug in VEHICULO_DATA.keys():
        result = result.replace(f'href="/vehiculos/{vslug}"', f'href="/en/vehiculos/{vslug}"')
    
    # Fix brand links
    for mslug in MARCA_DATA.keys():
        result = result.replace(f'href="/marcas_automotrices/{mslug}"', f'href="/en/marcas_automotrices/{mslug}"')
    
    # Fix logo link
    result = result.replace('href="/" class="logo', 'href="/en/" class="logo')
    result = result.replace('href="#inicio" class="logo', 'href="/en/" class="logo')
    
    # Fix WhatsApp
    result = result.replace('Hola%20necesito%20', 'Hi%20I%20need%20')
    result = result.replace('Hola,%20quiero%20cotizar%20por%20', 'Hi,%20I%20want%20a%20quote%20for%20')
    
    # Fix brand
    result = result.replace('GlobalPro Automotriz', 'GlobalPro Automotive')
    
    # Add language switcher
    result = add_language_switcher(result)
    
    # Fix canonical and hreflang for standalone
    # Remove old hreflang
    result = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\s*\n?', '', result)
    
    # Add correct hreflang
    if filename == 'index.html':
        es_url = 'https://mecanico247.com/'
        en_url = 'https://mecanico247.com/en/'
        result = result.replace(
            '<link rel="canonical" href="https://mecanico247.com/"/>',
            f'<link rel="canonical" href="{en_url}"/>\n<link rel="alternate" hreflang="es" href="{es_url}" />\n<link rel="alternate" hreflang="en" href="{en_url}" />\n<link rel="alternate" hreflang="x-default" href="{es_url}" />'
        )
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  OK: {en_path}")
    return True


def main():
    """Main function to process all pages."""
    os.chdir('/home/z/my-project/mecanico247')
    
    print("=" * 60)
    print("REWRITING ALL /en/ PAGES WITH PROPER ENGLISH")
    print("=" * 60)
    
    # Phase 1: Comuna pages (52)
    print("\n[Phase 1] Processing 52 comuna pages...")
    ok = 0
    for slug in COMUNA_DATA.keys():
        if process_comuna_page(slug):
            ok += 1
    print(f"  Completed: {ok}/52 comuna pages")
    
    # Phase 2: Vehicle pages (33)
    print("\n[Phase 2] Processing vehicle pages...")
    ok = 0
    for slug in VEHICULO_DATA.keys():
        en_path = f'en/vehiculos/{slug}.html'
        if os.path.exists(en_path):
            if process_vehiculo_page(slug):
                ok += 1
    print(f"  Completed: {ok} vehicle pages")
    
    # Phase 3: Service pages (7)
    print("\n[Phase 3] Processing service pages...")
    ok = 0
    for slug in SERVICIO_DATA.keys():
        if process_servicio_page(slug):
            ok += 1
    print(f"  Completed: {ok} service pages")
    
    # Phase 4: Brand pages (10)
    print("\n[Phase 4] Processing brand pages...")
    ok = 0
    for slug in os.listdir('en/marcas_automotrices/'):
        if slug.endswith('.html') and slug != 'index.html':
            s = slug.replace('.html', '')
            if process_marca_page(s):
                ok += 1
    print(f"  Completed: {ok} brand pages")
    
    # Phase 5: Standalone pages
    print("\n[Phase 5] Processing standalone pages...")
    standalone_files = ['index.html', 'about-us.html', 'contacto.html', 'faq.html', 
                        'privacy-policy.html', '404.html', 'mechanical-inspection.html', 
                        'services-at-home.html']
    ok = 0
    for filename in standalone_files:
        if os.path.exists(f'en/{filename}'):
            if process_standalone_page(filename):
                ok += 1
    print(f"  Completed: {ok} standalone pages")
    
    print("\n" + "=" * 60)
    print("REWRITE COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
