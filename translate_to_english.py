#!/usr/bin/env python3
"""
Comprehensive English translation script for mecanico247.com
Translates all Spanish pages to professional, natural English under /en/ directory.
"""

import os
import re
import shutil
import glob
import json

BASE = '/home/z/my-project/Globalpro'
EN_BASE = os.path.join(BASE, 'en')

# ============================================================
# STEP 1: Clean up existing /en/ content
# ============================================================
def cleanup_en():
    """Delete all /en/ content except /en/blog/ directory (keep dir, delete html files)"""
    print("=== Step 1: Cleaning up existing /en/ content ===")
    
    # Delete everything in /en/ except blog directory
    if os.path.exists(EN_BASE):
        for item in os.listdir(EN_BASE):
            item_path = os.path.join(EN_BASE, item)
            if item == 'blog':
                # Delete all HTML files in blog but keep directory
                for f in glob.glob(os.path.join(item_path, '*.html')):
                    os.remove(f)
                    print(f"  Deleted: {f}")
            else:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"  Removed dir: {item_path}")
                else:
                    os.remove(item_path)
                    print(f"  Deleted: {item_path}")
    
    # Create directory structure
    for d in ['comunas', 'servicios', 'vehiculos', 'marcas_automotrices', 'blog']:
        os.makedirs(os.path.join(EN_BASE, d), exist_ok=True)
    print("  Created /en/ directory structure")

# ============================================================
# LANGUAGE SWITCHER HTML
# ============================================================
def lang_switcher_en(en_path):
    """Return the language switcher HTML for English pages"""
    es_path = en_path.replace('/en/', '/').replace('/air-conditioning', '/aire-acondicionado-automotriz').replace('/oil-change-at-home', '/cambio-de-aceite-a-domicilio').replace('/brake-repair-at-home', '/cambio-de-frenos-a-domicilio').replace('/diagnostic-scan-at-home', '/diagnostico-con-scanner-a-domicilio').replace('/auto-electrical-at-home', '/electricidad-automotriz-a-domicilio').replace('/24-hour-mechanic', '/mecanico-24-horas').replace('/emergency-mechanic', '/mecanico-de-emergencia').replace('/about-us', '/quienes-somos').replace('/privacy-policy', '/politica-privacidad').replace('/mechanical-inspection', '/inspeccion-mecanica').replace('/services-at-home', '/servicios-domicilio')
    # Remove trailing .html if present
    es_path = es_path.replace('.html', '')
    # If path ends with just /en/ or index
    if es_path == '/' or es_path == '':
        es_path = '/'
    return '''<div id="lang-switcher" style="position:fixed; top:80px; right:15px; z-index:9999; display:flex; gap:4px;">
  <a href="{es_path}" style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; text-decoration:none;">🇪🇸 ES</a>
  <span style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700;">🇬🇧 EN</span>
</div>'''.format(es_path=es_path)

# ============================================================
# COMPREHENSIVE TEXT REPLACEMENTS
# ============================================================
# These replacements cover ALL Spanish text across the site

GLOBAL_REPLACEMENTS = [
    # Meta/HTML level
    ('lang="es-CL"', 'lang="en"'),
    ('og:locale" content="es_CL"', 'og:locale" content="en_US"'),
    
    # Logo subtitle
    ('Taller Mecánico', 'Auto Repair Shop'),
    ('Taller Mecanico', 'Auto Repair Shop'),
    
    # Navbar items
    ('Mecánico a Domicilio', 'Mobile Mechanic'),
    ('Mecanico a Domicilio', 'Mobile Mechanic'),
    ('>Servicios<', '>Services<'),
    ('>Comunas<', '>Areas<'),
    ('>Comunas ', '>Areas '),
    ('Quiénes Somos', 'About Us'),
    ('Quienes Somos', 'About Us'),
    ('>Contacto<', '>Contact<'),
    ('>Blog<', '>Blog<'),
    ('>Vehiculos<', '>Vehicles<'),
    ('>Vehículos<', '>Vehicles<'),
    ('>FAQ<', '>FAQ<'),
    ('>Privacidad<', '>Privacy<'),
    ('Inspección Mecánica', 'Mechanical Inspection'),
    ('Inspeccion Mecanica', 'Mechanical Inspection'),
    ('Servicios a Domicilio', 'Mobile Services'),
    ('Servicios Domicilio', 'Mobile Services'),
    
    # Hero section
    ('Servicio Automotriz Integral', 'Complete Automotive Service'),
    ('Servicio Automotriz a Domicilio', 'Mobile Automotive Service'),
    ('Autos Reparados', 'Cars Repaired'),
    ('Años de Experiencia', 'Years of Experience'),
    ('Garantía de Servicio', 'Service Guarantee'),
    ('Garantia de Servicio', 'Service Guarantee'),
    ('Clientes Atendidos', 'Customers Served'),
    ('Disponibilidad', 'Availability'),
    ('Cotizar por WhatsApp', 'Get a Quote on WhatsApp'),
    ('Ver Servicios', 'View Services'),
    ('Agenda tu Visita Tecnica', 'Schedule Your Visit'),
    ('Agenda tu Visita Técnica', 'Schedule Your Visit'),
    
    # Google Business Profile
    ('Ver Nuestro Perfil de Google', 'View Our Google Profile'),
    ('opiniones verificadas', 'verified reviews'),
    ('155+ opiniones verificadas', '155+ verified reviews'),
    
    # SEO Section
    ('El Mejor', 'The Best'),
    ('Solución Inmediata', 'Immediate Solution'),
    ('Servicio Profesional de', 'Professional'),
    ('para toda la Región Metropolitana', 'Across the Metropolitan Region'),
    ('Auto Repair Shops Near Me', 'Auto Repair Shops Near Me'),
    
    # SEO H1/H2 patterns
    ('Mecánico a Domicilio</span> en', 'Mobile Mechanic</span> in'),
    ('Mecanico a Domicilio</span> en', 'Mobile Mechanic</span> in'),
    
    # Featured oil change section
    ('Servicio Más Buscado', 'Most Popular Service'),
    ('Cambio de Aceite', 'Oil Change'),
    ('A Domicilio', 'Mobile Service'),
    ('Sintético Premium', 'Premium Synthetic'),
    ('Filtro Incluido', 'Filter Included'),
    ('Agenda Rápido', 'Quick Scheduling'),
    ('Agenda Tu Cambio de Aceite Ya', 'Schedule Your Oil Change Now'),
    ('Agenda Tu Cambio de Aceite', 'Schedule Your Oil Change'),
    ('cambio de aceite cerca mio', 'oil change near me'),
    
    # Servicios destacados
    ('Servicios Más Solicitados', 'Most Requested Services'),
    ('Servicios Mas Solicitados', 'Most Requested Services'),
    ('Los servicios que más necesitan', 'The services most needed by'),
    ('Los servicios mas necesitados', 'The services most needed by'),
    ('Agenda rápido por WhatsApp', 'Schedule quickly on WhatsApp'),
    ('Nuestros servicios estrella', 'Our star services'),
    ('Aceites sintéticos y semi-sintéticos premium', 'Premium synthetic and semi-synthetic oils'),
    ('Aceites sinteticos y semi-sinteticos premium', 'Premium synthetic and semi-synthetic oils'),
    ('Incluye filtro y revisión de niveles', 'Includes filter and fluid level check'),
    ('Incluye filtro y revision de niveles', 'Includes filter and fluid level check'),
    ('A domicilio en', 'Mobile service in'),
    ('Pastillas, discos, líquido y ABS', 'Pads, rotors, fluid and ABS'),
    ('Pastillas, discos, liquido y ABS', 'Pads, rotors, fluid and ABS'),
    ('Medición digital del espesor', 'Digital thickness measurement'),
    ('Medicion digital del espesor', 'Digital thickness measurement'),
    ('Tu seguridad es primero', 'Your safety comes first'),
    ('Electricidad', 'Electrical'),
    ('Diagnóstico eléctrico completo', 'Complete electrical diagnosis'),
    ('Diagnostico electrico completo', 'Complete electrical diagnosis'),
    ('Batería, alternador, motor de arranque y cableado', 'Battery, alternator, starter motor and wiring'),
    ('Bateria, alternador, motor de arranque y cableado', 'Battery, alternator, starter motor and wiring'),
    ('Escáner', 'Diagnostics'),
    ('Escanner', 'Diagnostics'),
    ('Diagnóstico computarizado sin adivinanzas', 'Computerized diagnostics, no guesswork'),
    ('Diagnostico computarizado sin adivinanzas', 'Computerized diagnostics, no guesswork'),
    ('Interpretación de códigos y soluciones reales', 'Code interpretation and real solutions'),
    ('Interpretacion de codigos y soluciones reales', 'Code interpretation and real solutions'),
    
    # Reviews section
    ('Lo que dicen nuestros clientes', 'What Our Customers Say'),
    ('Tu confianza es nuestra mejor carta de presentación', 'Your trust is our best endorsement'),
    ('Tu confianza es nuestra mejor carta de presentacion', 'Your trust is our best endorsement'),
    ('Lee las experiencias de quienes ya confían en nuestro trabajo', 'Read the experiences of those who already trust our work'),
    ('Lee las experiencias de quienes ya confian en nuestro trabajo', 'Read the experiences of those who already trust our work'),
    
    # Conectamos marquee section
    ('Conectamos a propietarios de vehículos con especialistas en mantenciones, revisiones y reparaciones específicas de tu auto en donde lo necesites', 'We connect vehicle owners with maintenance, inspection, and repair specialists wherever you need them'),
    ('Conectamos a propietarios de vehiculos con especialistas en mantenciones, revisiones y reparaciones especificas de tu auto en donde lo necesites', 'We connect vehicle owners with maintenance, inspection, and repair specialists wherever you need them'),
    ('Atención a domicilio en las comunas de la RM', 'Mobile service across Santiago metropolitan area'),
    ('Atencion a domicilio en las comunas de la RM', 'Mobile service across Santiago metropolitan area'),
    ('+52 marcas atendidas en Santiago', '52+ brands served in Santiago'),
    ('Marca automotriz', 'Automotive brand'),
    
    # Services section
    ('Nuestros Servicios de Mecánica Automotriz', 'Our Auto Repair Services'),
    ('Ofrecemos una solución completa para el mantenimiento y reparación de tu vehículo', 'We offer a complete solution for your vehicle maintenance and repair'),
    ('Mecánica General y Mantenimiento', 'General Mechanics & Maintenance'),
    ('Electromecánica y Electricidad', 'Electromechanics & Electrical'),
    ('Chapa y Pintura Automotriz', 'Bodywork & Paint'),
    ('Aire Acondicionado y Calefacción', 'Air Conditioning & Heating'),
    ('Frenos y Suspensión', 'Brakes & Suspension'),
    ('Reparación de Transmisión', 'Transmission Repair'),
    ('Sistema de Escape y Turbos', 'Exhaust System & Turbos'),
    ('Sistemas de Gas GNV/GLP', 'CNG/LPG Gas Systems'),
    ('Diagnóstico Computarizado', 'Computerized Diagnostics'),
    ('Servicio a Domicilio', 'Mobile Service'),
    
    # Service descriptions
    ('mantenimiento preventivo', 'preventive maintenance'),
    ('engrase general', 'general lubrication'),
    ('cambio de aceite', 'oil change'),
    ('revisión técnica', 'technical inspection'),
    ('revision tecnica', 'technical inspection'),
    ('electricidad automotriz', 'auto electrical'),
    ('reparación de ECU', 'ECU repair'),
    ('diagnóstico de fallas eléctricas', 'electrical fault diagnosis'),
    ('sistema de inyección', 'injection system'),
    ('reparación de carrocería', 'bodywork repair'),
    ('chapa y pintura', 'bodywork and paint'),
    ('reparación de interiores y tapicería', 'interior and upholstery repair'),
    ('Reparación y mantenimiento de aire acondicionado auto', 'Auto AC repair and maintenance'),
    ('Carga de gas', 'Gas recharge'),
    ('reparación de frenos', 'brake repair'),
    ('suspensión', 'suspension'),
    ('dirección', 'steering'),
    ('transmisiones manuales y automáticas', 'manual and automatic transmissions'),
    ('embrague', 'clutch'),
    ('caja de transferencia', 'transfer case'),
    ('diferencial', 'differential'),
    ('escapes de autos', 'exhaust systems'),
    ('reparación de turbos', 'turbo repair'),
    ('catalizador', 'catalytic converter'),
    ('silenciador', 'muffler'),
    ('Instalación, certificación y reparación de sistemas de gas para vehículos', 'Installation, certification and repair of vehicle gas systems'),
    ('scanner automotriz', 'automotive scanner'),
    ('diagnóstico avanzado de fallas', 'advanced fault diagnosis'),
    ('servicio mecánico a domicilio', 'mobile mechanical service'),
    ('auxilio en carretera', 'roadside assistance'),
    
    # COTIZAR / Quote buttons
    ('Cotizar Ahora', 'Get a Quote'),
    ('Cotizar', 'Get a Quote'),
    ('Cotizar Servicio en', 'Get a Service Quote in'),
    ('Cotizar Calefaccion Ahora', 'Get a Heating Quote Now'),
    
    # Calefacción section
    ('Servicio Avanzado de Climatizacion y Calefaccion Automotriz 24/7', 'Advanced Vehicle Climate Control & Heating Service 24/7'),
    ('calefaccion para vehiculos', 'vehicle heating systems'),
    ('calefaccion para autos', 'heating for cars'),
    ('calefaccion para furgoneta', 'van heating'),
    ('calefaccion en el coche', 'car heating'),
    ('calefaccion de coche', 'car heater'),
    ('calefaccion coche', 'car heater'),
    ('calefaccion estacionaria coche', 'stationary car heater'),
    ('calefaccion estacionaria para camiones', 'stationary heater for trucks'),
    ('calefaccion para camion', 'truck heater'),
    ('calefaccion furgoneta', 'van heater'),
    ('calefaccion furgoneta 12v', '12v van heater'),
    ('calefaccion portatil furgoneta', 'portable van heater'),
    ('calefaccion diesel motorhome', 'diesel motorhome heater'),
    ('calefaccion estacionaria caravana', 'stationary caravan heater'),
    ('calefaccion para autocaravana', 'motorhome heater'),
    ('calefaccion para casa rodante', 'RV heater'),
    ('calefaccion de vehiculos', 'vehicle heating'),
    ('calefaccion estatica furgoneta', 'static van heater'),
    ('calefaccion para furgonetas camper', 'camper van heater'),
    ('calefaccion electrica furgoneta', 'electric van heater'),
    ('calefaccion electrica para automoviles', 'electric heater for cars'),
    ('calefaccion electrica para coche', 'electric car heater'),
    ('calefaccion auxiliar para coche', 'auxiliary car heater'),
    ('calefaccion auxiliar para furgonetas', 'auxiliary van heater'),
    ('calefaccion autonoma coche', 'autonomous car heater'),
    ('calefaccion asiento coche', 'seat heater'),
    ('calefaccion en asientos coche', 'heated seats'),
    ('calefaccion bateria coche', 'car battery heater'),
    ('resistencia calefaccion peugeot 207', 'Peugeot 207 heater resistor'),
    ('calefaccion de autos', 'car heating'),
    ('calefaccion autos', 'car heating'),
    ('calefaccion carro', 'car heater'),
    ('calefaccion vehiculos', 'vehicle heating'),
    ('calefaccion para coche', 'car heater'),
    ('calefaccion para autos portatil', 'portable car heater'),
    
    # Calefacción paragraphs (longer text blocks)
    ('Si tu sistema esta fallando o necesitas mejorar el confort de tu viaje en Santiago, nuestro equipo tecnico cuenta con unidades de respuesta rapida. Nos especializamos en el diagnostico, reparacion e instalacion de',
     'If your system is failing or you need to improve your driving comfort in Santiago, our technical team has rapid response units. We specialize in the diagnosis, repair and installation of'),
    ('directamente en tu ubicacion. Cuando las bajas temperaturas se hacen sentir, garantizamos que la calefaccion en el coche o la calefaccion de coche funcione a su maxima capacidad y con total seguridad.',
     'directly at your location. When temperatures drop, we ensure your car heating system works at maximum capacity with complete safety.'),
    ('Sabemos que cada tipo de transporte requiere una solucion tecnica diferente. Por eso, nuestros tecnicos capacitados manejan a la perfeccion desde sistemas tradicionales de',
     'We know that each type of vehicle requires a different technical solution. That is why our trained technicians expertly handle everything from traditional'),
    ('hasta tecnologias especificas como la',
     'systems to specific technologies like'),
    ('Ademas, si eres amante de los viajes y la vida en ruta, resolvemos cualquier problema de',
     'Additionally, if you love road trips and life on the go, we solve any issues with'),
    ('garantizando el clima ideal mediante sistemas especializados como la',
     'ensuring ideal climate through specialized systems like'),
    ('Para quienes camperizan sus vehiculos, entregamos soluciones eficientes en',
     'For those who convert their vehicles into campers, we provide efficient solutions for'),
    ('Atendemos fallas complejas de eficiencia energetica, evaluando si la calefaccion coche consume gasolina en exceso o si es mejor implementar alternativas modernas como la',
     'We address complex energy efficiency issues, evaluating whether the car heater consumes excessive fuel or if it is better to implement modern alternatives like'),
    ('Asimismo, optimizamos sistemas pesados configurando',
     'Likewise, we optimize heavy-duty systems by configuring'),
    ('para un rendimiento continuo.',
     'for continuous performance.'),
    ('El confort termico interior tambien abarca los componentes electricos directos. Resolvemos desperfectos en la',
     'Interior thermal comfort also involves direct electrical components. We fix issues with'),
    ('y en la distribucion de energia como la',
     'and in power distribution such as'),
    ('Nuestros mecanicos cuentan con el equipamiento para sustituir componentes especificos del habitaculo, incluyendo fallas comunes de climatizacion multimarca como la',
     'Our mechanics have the equipment to replace specific interior components, including common multi-brand climate control failures like'),
    ('No arriesgues la comodidad de tus pasajeros; si buscas optimizar la',
     "Don't risk your passengers' comfort; if you want to optimize"),
    ('o requieres una',
     'or need a'),
    ('traditional or a',
     'traditional or a'),
    ('activa tu Orden Express ahora.',
     'activate your Express Order now.'),
    
    # Detailed services section
    ('Servicios Mecanicos en', 'Mechanical Services in'),
    ('Servicios Mecánicos en', 'Mechanical Services in'),
    ('Todos los servicios automotrices que necesitas directamente en tu comuna, sin moverte de casa', 'All the automotive services you need right in your area, without leaving home'),
    
    # Detailed service block titles
    ('Mecanico a Domicilio en', 'Mobile Mechanic in'),
    ('Scanner Automotriz en', 'Automotive Diagnostics in'),
    ('Frenos y Pastillas en', 'Brakes & Pads in'),
    ('Cambio de Aceite en', 'Oil Change in'),
    ('Alineamiento y Suspension en', 'Alignment & Suspension in'),
    ('Reparacion de Motores en', 'Engine Repair in'),
    ('Embrague y Correa de Distribucion en', 'Clutch & Timing Belt in'),
    ('Servicio de Bateria y Electricidad en', 'Battery & Electrical Service in'),
    ('Cambio de Bujias y Mantencion en', 'Spark Plug Replacement & Maintenance in'),
    ('Emergencias 24/7 y Taller Mecanico Cerca de Mi', '24/7 Emergencies & Auto Repair Shop Near Me'),
    
    # How It Works section
    ('COMO FUNCIONA NUESTRO SERVICIO DE MECÁNICA A DOMICILIO', 'HOW OUR MOBILE MECHANIC SERVICE WORKS'),
    ('COMO FUNCIONA NUESTRO SERVICIO DE MECANICA A DOMICILIO', 'HOW OUR MOBILE MECHANIC SERVICE WORKS'),
    ('Nuestro proceso es simple, rápido y pensado para que no pierdas tiempo', 'Our process is simple, fast, and designed so you don\'t waste time'),
    ('Nuestro proceso es simple, rapido y pensado para que no pierdas tiempo', 'Our process is simple, fast, and designed so you don\'t waste time'),
    ('COTIZA', 'GET A QUOTE'),
    ('AGENDA', 'SCHEDULE'),
    ('TU AUTO LISTO EN 2 HORAS', 'YOUR CAR READY IN 2 HOURS'),
    ('Escríbenos al WhatsApp y cotiza tu servicio', 'Message us on WhatsApp and get a quote'),
    ('Escribenos al WhatsApp y cotiza tu servicio', 'Message us on WhatsApp and get a quote'),
    ('de forma rápida y sin compromiso', 'quickly and with no obligation'),
    ('de forma rapida y sin compromiso', 'quickly and with no obligation'),
    ('Agendamos tu servicio en el horario que más te acomode', 'We schedule your service at the time that works best for you'),
    ('Agendamos tu servicio en el horario que mas te acomode', 'We schedule your service at the time that works best for you'),
    ('Nuestro técnico se desplaza a tu ubicación', 'Our technician comes to your location'),
    ('Nuestro tecnico se desplaza a tu ubicacion', 'Our technician comes to your location'),
    ('En menos de 2 horas tu vehículo queda listo', 'In less than 2 hours your vehicle is ready'),
    ('En menos de 2 horas tu vehiculo queda listo', 'In less than 2 hours your vehicle is ready'),
    
    # Why Choose Us section
    ('Por Qué Elegirnos', 'Why Choose Us'),
    ('Por Que Elegirnos', 'Why Choose Us'),
    ('Taller Móvil Equipado', 'Equipped Mobile Workshop'),
    ('Taller Movil Equipado', 'Equipped Mobile Workshop'),
    ('Llevamos herramientas profesionales y equipos de diagnóstico directamente a tu ubicación', 'We bring professional tools and diagnostic equipment directly to your location'),
    ('Llevamos herramientas profesionales y equipos de diagnostico directamente a tu ubicacion', 'We bring professional tools and diagnostic equipment directly to your location'),
    ('Respuesta Rápida', 'Fast Response'),
    ('Respuesta Rapida', 'Fast Response'),
    ('En menos de 60 minutos un técnico puede estar contigo en caso de emergencia', 'A technician can be with you in under 60 minutes in case of emergency'),
    ('En menos de 60 minutos un tecnico puede estar contigo en caso de emergencia', 'A technician can be with you in under 60 minutes in case of emergency'),
    ('Técnicos Certificados', 'Certified Technicians'),
    ('Tecnicos Certificados', 'Certified Technicians'),
    ('Nuestro equipo cuenta con certificaciones y años de experiencia en todas las marcas', 'Our team holds certifications and years of experience with all brands'),
    ('Nuestro equipo cuenta con certificaciones y anos de experiencia en todas las marcas', 'Our team holds certifications and years of experience with all brands'),
    ('Garantía en Todos los Servicios', 'Warranty on All Services'),
    ('Garantia en Todos los Servicios', 'Warranty on All Services'),
    ('Ofrecemos garantía de 3 a 12 meses dependiendo del tipo de reparación', 'We offer a 3 to 12-month warranty depending on the type of repair'),
    ('Ofrecemos garantia de 3 a 12 meses dependiendo del tipo de reparacion', 'We offer a 3 to 12-month warranty depending on the type of repair'),
    ('Precios Transparentes', 'Transparent Pricing'),
    ('Presupuesto sin compromiso antes de iniciar cualquier reparación', 'No-obligation quote before starting any repair'),
    ('Presupuesto sin compromiso antes de iniciar cualquier reparacion', 'No-obligation quote before starting any repair'),
    ('Disponibilidad 24/7', '24/7 Availability'),
    ('Atendemos emergencias mecánicas las 24 horas del día, los 7 días de la semana', 'We handle mechanical emergencies 24 hours a day, 7 days a week'),
    ('Atendemos emergencias mecanicas las 24 horas del dia, los 7 dias de la semana', 'We handle mechanical emergencies 24 hours a day, 7 days a week'),
    
    # FAQ section
    ('Preguntas Frecuentes', 'Frequently Asked Questions'),
    
    # Footer
    ('Somos líderes en', 'We are leaders in'),
    ('en Santiago', 'in Santiago'),
    ('Ofrecemos servicio automotriz integral con tecnología de punta y profesionales certificados', 'We offer complete automotive service with cutting-edge technology and certified professionals'),
    ('Ofrecemos servicio automotriz integral con tecnologia de punta y profesionales certificados', 'We offer complete automotive service with cutting-edge technology and certified professionals'),
    ('Tu vehículo en las mejores manos, donde tú estés', 'Your vehicle in the best hands, wherever you are'),
    ('Tu vehiculo en las mejores manos, donde tu estes', 'Your vehicle in the best hands, wherever you are'),
    ('Enlaces Rápidos', 'Quick Links'),
    ('Enlaces Rapidos', 'Quick Links'),
    ('Inicio', 'Home'),
    ('Nuestros Servicios', 'Our Services'),
    ('Información de Contacto', 'Contact Information'),
    ('Informacion de Contacto', 'Contact Information'),
    ('Ubicación:', 'Location:'),
    ('Servicio a Domicilio en todo Santiago', 'Mobile service across Santiago'),
    ('Base: Pedro Aguirre Cerda, RM', 'Base: Pedro Aguirre Cerda, RM'),
    ('Teléfono:', 'Phone:'),
    ('Email:', 'Email:'),
    ('Todos los derechos reservados', 'All rights reserved'),
    ('Especialistas en', 'Specialists in'),
    ('Servicio Automotriz Integral', 'Complete Automotive Service'),
    
    # Sticky bottom bar
    ('LLAMAR', 'CALL'),
    ('TU AUTO LISTO', 'YOUR CAR READY'),
    ('EN 2 HORAS', 'IN 2 HOURS'),
    
    # WhatsApp messages
    ('Hola%20necesito%20un%20mecanico%20a%20domicilio%20en%20', 'Hello%20I%20need%20a%20mobile%20mechanic%20in%20'),
    ('Hola%20necesito%20un%20cambio%20de%20aceite%20a%20domicilio%20en%20', 'Hello%20I%20need%20an%20oil%20change%20at%20home%20in%20'),
    ('Hola%20necesito%20reparacion%20de%20frenos%20a%20domicilio%20en%20', 'Hello%20I%20need%20brake%20repair%20at%20home%20in%20'),
    ('Hola%20necesito%20electricidad%20automotriz%20a%20domicilio%20en%20', 'Hello%20I%20need%20auto%20electrical%20service%20at%20home%20in%20'),
    ('Hola%20necesito%20scanner%20automotriz%20a%20domicilio%20en%20', 'Hello%20I%20need%20a%20diagnostic%20scan%20at%20home%20in%20'),
    ('Hola%20necesito%20servicio%20de%20calefaccion%20automotriz%20en%20', 'Hello%20I%20need%20vehicle%20heating%20service%20in%20'),
    ('Hola,%20quiero%20cotizar%20por%20', 'Hello,%20I%20want%20a%20quote%20for%20'),
    ('Hola%20te%20escribo%20desde%20la%20página%20web%20estoy%20interesado%20en%20tus%20servicios', 'Hello%20I%20am%20writing%20from%20the%20website%20I%20am%20interested%20in%20your%20services'),
    ('Hola%20te%20escribo%20desde%20la%20pagina%20web%20estoy%20interesado%20en%20tus%20servicios', 'Hello%20I%20am%20writing%20from%20the%20website%20I%20am%20interested%20in%20your%20services'),
    ('Hola%20necesito%20un%20mecánico%20de%20urgencia', 'Hello%20I%20need%20an%20emergency%20mechanic'),
    ('Hola%20tengo%20una%20consulta%20sobre%20los%20servicios%20de%20GlobalPro', 'Hello%20I%20have%20a%20question%20about%20GlobalPro%20services'),
    ('Hola%20vi%20su%20rating%20en%20Google%20y%20quiero%20agendar%20un%20servicio', 'Hello%20I%20saw%20your%20Google%20rating%20and%20want%20to%20schedule%20a%20service'),
    
    # Visitantes counter
    ('Visitantes', 'Visitors'),
    
    # Brands section
    ('Trabajamos con todas las marcas', 'We work with all brands'),
    
    # Other common terms
    ('servicio automotriz', 'automotive service'),
    ('mecánico a domicilio', 'mobile mechanic'),
    ('mecanico a domicilio', 'mobile mechanic'),
    ('taller mecánico', 'auto repair shop'),
    ('taller mecanico', 'auto repair shop'),
    ('Región Metropolitana', 'Metropolitan Region'),
    ('Region Metropolitana', 'Metropolitan Region'),
    ('Santiago de Chile', 'Santiago, Chile'),
    ('sin compromiso', 'no obligation'),
    ('sin costos ocultos', 'no hidden costs'),
    ('a domicilio', 'mobile service'),
    ('a tu domicilio', 'at your location'),
    ('en tu domicilio', 'at your location'),
    ('más de 5.000 clientes satisfechos', 'over 5,000 satisfied customers'),
    ('mas de 5.000 clientes satisfechos', 'over 5,000 satisfied customers'),
    ('más de 5,000 clientes satisfechos', 'over 5,000 satisfied customers'),
    ('mas de 5,000 clientes satisfechos', 'over 5,000 satisfied customers'),
    ('+5.000 clientes atendidos', '5,000+ customers served'),
    ('+5,000 clientes atendidos', '5,000+ customers served'),
    ('Cotiza por WhatsApp', 'Get a Quote on WhatsApp'),
    ('Agendar Servicio Ahora', 'Schedule Service Now'),
    ('Escribir por WhatsApp', 'Message on WhatsApp'),
    ('Llamar Ahora', 'Call Now'),
    ('LLAMAR AHORA', 'CALL NOW'),
    ('WHATSAPP DE EMERGENCIA', 'EMERGENCY WHATSAPP'),
    ('¿Necesitas un mecánico', 'Need a mechanic'),
    ('¿Necesitas un mecanico', 'Need a mechanic'),
    ('AHORA MISMO', 'RIGHT NOW'),
    ('No esperes más', "Don't wait any longer"),
    ('No esperes mas', "Don't wait any longer"),
    ('Nuestro equipo está listo para ayudarte en cualquier momento y lugar de Santiago', 'Our team is ready to help you anytime, anywhere in Santiago'),
    ('Nuestro equipo esta listo para ayudarte en cualquier momento y lugar de Santiago', 'Our team is ready to help you anytime, anywhere in Santiago'),
    ('Horario de Atención', 'Business Hours'),
    ('Lunes a Domingo', 'Monday to Sunday'),
    ('ABIERTO LAS 24 HORAS', 'OPEN 24 HOURS'),
    ('Emergencias mecánicas en cualquier momento del día o la noche', 'Mechanical emergencies at any time of day or night'),
    ('Emergencias mecanicas en cualquier momento del dia o la noche', 'Mechanical emergencies at any time of day or night'),
    ('o escríbenos por WhatsApp', 'or message us on WhatsApp'),
    ('o escribenos por WhatsApp', 'or message us on WhatsApp'),
    
    # Contact page specific
    ('Contáctanos', 'Contact Us'),
    ('Contactanos', 'Contact Us'),
    ('Estamos disponibles las 24 horas, los 7 días de la semana', 'We are available 24 hours a day, 7 days a week'),
    ('Estamos disponibles las 24 horas, los 7 dias de la semana', 'We are available 24 hours a day, 7 days a week'),
    ('Llámanos, escríbenos por WhatsApp o visita nuestro taller', 'Call us, message us on WhatsApp or visit our shop'),
    ('Llamanos, escribenos por WhatsApp o visita nuestro taller', 'Call us, message us on WhatsApp or visit our shop'),
    ('Elige Cómo Contactarnos', 'Choose How to Contact Us'),
    ('Elige Como Contactarnos', 'Choose How to Contact Us'),
    ('Múltiples opciones para que nos reachen fácil y rápidamente', 'Multiple options to reach us easily and quickly'),
    ('Multiples opciones para que nos reachen facil y rapidamente', 'Multiple options to reach us easily and quickly'),
    ('Atención inmediata garantizada', 'Immediate attention guaranteed'),
    ('Atencion inmediata garantizada', 'Immediate attention guaranteed'),
    ('Llámanos', 'Call Us'),
    ('Llamanos', 'Call Us'),
    ('Habla directamente con nuestro equipo de atención al cliente', 'Speak directly with our customer service team'),
    ('Habla directamente con nuestro equipo de atencion al cliente', 'Speak directly with our customer service team'),
    ('Escríbenos y recibe respuesta inmediata', 'Message us and get an immediate response'),
    ('Escribenos y recibe respuesta inmediata', 'Message us and get an immediate response'),
    ('Envía fotos de tu vehículo', 'Send photos of your vehicle'),
    ('Envia fotos de tu vehiculo', 'Send photos of your vehicle'),
    ('Enviar Mensaje', 'Send Message'),
    ('Para cotizaciones formales, consultas o información detallada', 'For formal quotes, inquiries or detailed information'),
    ('Para cotizaciones formales, consultas o informacion detallada', 'For formal quotes, inquiries or detailed information'),
    ('Visítanos', 'Visit Us'),
    ('Visitanos', 'Visit Us'),
    ('Nuestro taller está ubicado en Pedro Aguirre Cerda, Santiago', 'Our shop is located in Pedro Aguirre Cerda, Santiago'),
    ('Nuestro taller esta ubicado en Pedro Aguirre Cerda, Santiago', 'Our shop is located in Pedro Aguirre Cerda, Santiago'),
    ('Ver en Google Maps', 'View on Google Maps'),
    ('Nuestra Ubicación', 'Our Location'),
    ('Nuestra Ubicacion', 'Our Location'),
    ('Envíanos un Mensaje', 'Send Us a Message'),
    ('Envianos un Mensaje', 'Send Us a Message'),
    ('Cuéntanos sobre tu vehículo y el servicio que necesitas', 'Tell us about your vehicle and the service you need'),
    ('Cuentanos sobre tu vehiculo y el servicio que necesitas', 'Tell us about your vehicle and the service you need'),
    ('Te responderemos a la brevedad', 'We will respond shortly'),
    ('Nombre Completo', 'Full Name'),
    ('Teléfono', 'Phone'),
    ('Marca y Modelo del Vehículo', 'Vehicle Make and Model'),
    ('Servicio Necesitado', 'Service Needed'),
    ('Selecciona un servicio...', 'Select a service...'),
    ('Mecánica General', 'General Mechanics'),
    ('Diagnóstico Computarizado', 'Computerized Diagnostics'),
    ('Diagnostico Computarizado', 'Computerized Diagnostics'),
    ('Cambio de Aceite y Filtros', 'Oil & Filter Change'),
    ('Reparación de Frenos', 'Brake Repair'),
    ('Reparacion de Frenos', 'Brake Repair'),
    ('Reparación de Suspensión', 'Suspension Repair'),
    ('Reparacion de Suspension', 'Suspension Repair'),
    ('Sistema Eléctrico', 'Electrical System'),
    ('Sistema Electrico', 'Electrical System'),
    ('Cambio de Batería', 'Battery Replacement'),
    ('Cambio de Bateria', 'Battery Replacement'),
    ('Reparación de Motor', 'Engine Repair'),
    ('Reparacion de Motor', 'Engine Repair'),
    ('Reparación de Transmisión/Caja', 'Transmission Repair'),
    ('Reparacion de Transmision/Caja', 'Transmission Repair'),
    ('Aire Acondicionado', 'Air Conditioning'),
    ('Revisión Técnica', 'Technical Inspection'),
    ('Revision Tecnica', 'Technical Inspection'),
    ('Mantención Preventiva', 'Preventive Maintenance'),
    ('Mantencion Preventiva', 'Preventive Maintenance'),
    ('Electromecánica', 'Electromechanics'),
    ('Soldadura y Estructura', 'Welding & Structure'),
    ('Asistencia en Ruta / Emergencia', 'Roadside Assistance / Emergency'),
    ('Asistencia en Ruta', 'Roadside Assistance'),
    ('Inspección Pre-compra', 'Pre-Purchase Inspection'),
    ('Inspeccion Pre-compra', 'Pre-Purchase Inspection'),
    ('Otro', 'Other'),
    ('Mensaje', 'Message'),
    ('Describe el problema de tu vehículo o lo que necesitas...', 'Describe your vehicle issue or what you need...'),
    ('Describe el problema de tu vehiculo o lo que necesitas...', 'Describe your vehicle issue or what you need...'),
    ('Enviar Mensaje', 'Send Message'),
    ('Tu información está segura con nosotros', 'Your information is safe with us'),
    ('Tu informacion esta segura con nosotros', 'Your information is safe with us'),
    ('Nuevo mensaje desde GlobalPro - Contacto Web', 'New message from GlobalPro - Web Contact'),
    
    # About Us page specific
    ('Conoce la historia detras de GLOBAL PRO Automotriz', 'Discover the story behind GLOBAL PRO Automotive'),
    ('el servicio de mecanico a domicilio mas confiable de Santiago', 'the most reliable mobile mechanic service in Santiago'),
    ('Somos un taller de reparacion de automoviles', 'We are an auto repair shop'),
    ('con mas de 15 anos de experiencia', 'with over 15 years of experience'),
    ('en el mercado automotriz chileno', 'in the Chilean automotive market'),
    ('Nos especializamos en brindar un servicio de mecanico a domicilio 24/7', 'We specialize in providing 24/7 mobile mechanic service'),
    ('en toda la Region Metropolitana de Santiago', 'throughout the Santiago Metropolitan Region'),
    ('con sede en Pedro Aguirre Cerda', 'based in Pedro Aguirre Cerda'),
    ('Nuestro equipo de tecnicos certificados esta capacitado para resolver cualquier problema mecanico, electrico o de frenos que presente tu vehiculo', 'Our team of certified technicians is trained to solve any mechanical, electrical or brake problem your vehicle may have'),
    ('Desde un cambio de aceite hasta una reparacion compleja de motor', 'From an oil change to a complex engine repair'),
    ('nos desplazamos hasta donde tu estes con todas las herramientas y equipos de diagnostico necesarios', 'we come to wherever you are with all the necessary tools and diagnostic equipment'),
    ('En GLOBAL PRO Automotriz, creemos que la comodidad del cliente es primordial', 'At GLOBAL PRO Automotive, we believe customer convenience is paramount'),
    ('Por eso, llevamos el taller hasta tu puerta, ahorrandote tiempo, esfuerzo y dinero', 'That is why we bring the shop to your door, saving you time, effort and money'),
    ('Nuestros mas de 1000 autos reparados y la confianza de cientos de clientes satisfechos respaldan nuestro compromiso con la excelencia', 'Our 1,000+ repaired vehicles and the trust of hundreds of satisfied customers back our commitment to excellence'),
    ('Ubicacion Estrategica', 'Strategic Location'),
    ('Especialistas en Motor, Frenos y Electricidad', 'Engine, Brakes & Electrical Specialists'),
    ('Diagnostico computarizado y reparacion de cualquier sistema automotriz', 'Computerized diagnostics and repair of any automotive system'),
    ('Disponibles 24 Horas, 7 Dias', 'Available 24 Hours, 7 Days'),
    ('Emergencias mecanicas en cualquier momento del dia o la noche', 'Mechanical emergencies at any time of day or night'),
    ('Rating Google', 'Google Rating'),
    ('Siempre Disponibles', 'Always Available'),
    ('Nuestra Mision y Vision', 'Our Mission & Vision'),
    ('Los pilares que guian cada servicio que realizamos para nuestros clientes', 'The pillars that guide every service we provide for our customers'),
    ('Nuestra Mision', 'Our Mission'),
    ('Brindar un servicio automotriz de excelencia, accesible y confiable a todos los conductores de Santiago', 'To provide excellent, accessible and reliable automotive service to all drivers in Santiago'),
    ('Nos comprometemos a llevar la mejor atencion mecanica directamente al lugar donde se encuentre tu vehiculo', 'We are committed to bringing the best mechanical care directly to where your vehicle is located'),
    ('resolviendo problemas de motor, frenos y electricidad con rapidez, profesionalismo y garantia', 'solving engine, brake and electrical problems with speed, professionalism and warranty'),
    ('Nuestro objetivo es que cada cliente experimente tranquilidad y seguridad en cada intervencion', 'Our goal is for every customer to experience peace of mind and safety with every service'),
    ('Nuestra Vision', 'Our Vision'),
    ('Ser el referente numero uno en servicios de mecanica a domicilio en Chile', 'To be the number one reference in mobile mechanic services in Chile'),
    ('reconocidos por nuestra calidad tecnica, innovacion constante y compromiso con la satisfaccion total del cliente', 'recognized for our technical quality, constant innovation and commitment to total customer satisfaction'),
    ('Aspiramos a expandir nuestra cobertura a lo largo de todo el pais', 'We aspire to expand our coverage throughout the country'),
    ('manteniendo siempre los estandares de calidad y transparencia que nos caracterizan', 'always maintaining the quality and transparency standards that define us'),
    ('Nuestros Valores', 'Our Values'),
    ('Los principios que definen nuestro trabajo diario y nuestra relacion con cada cliente', 'The principles that define our daily work and our relationship with each customer'),
    ('Profesionalismo', 'Professionalism'),
    ('Cada uno de nuestros tecnicos cuenta con certificacion y anos de experiencia', 'Each of our technicians holds certification and years of experience'),
    ('Trabajamos con estandares profesionales en cada diagnostico y reparacion, garantizando resultados excepcionales', 'We work with professional standards in every diagnosis and repair, guaranteeing exceptional results'),
    ('Transparencia', 'Transparency'),
    ('Creemos en la comunicacion abierta con nuestros clientes', 'We believe in open communication with our customers'),
    ('Cada presupuesto es claro y detallado, sin costos ocultos ni sorpresas', 'Every quote is clear and detailed, with no hidden costs or surprises'),
    ('Tu apruebas cada reparacion antes de que la realicemos', 'You approve every repair before we carry it out'),
    ('Calidad', 'Quality'),
    ('Utilizamos repuestos de primera calidad y herramientas de diagnostico de ultima generacion', 'We use premium quality parts and state-of-the-art diagnostic tools'),
    ('Cada servicio queda respaldado por nuestra garantia, porque confiamos plenamente en lo que hacemos', 'Every service is backed by our warranty, because we fully trust what we do'),
    ('Compromiso', 'Commitment'),
    ('Nos comprometemos con tu seguridad y la de tu vehiculo', 'We are committed to your safety and that of your vehicle'),
    ('Disponibles las 24 horas del dia, los 7 dias de la semana, porque entendemos que una emergencia mecanica no espera', 'Available 24 hours a day, 7 days a week, because we understand a mechanical emergency cannot wait'),
    ('Respaldo de Nuestros Clientes', 'Endorsement from Our Customers'),
    ('La mejor prueba de nuestro trabajo son las opiniones de quienes ya confiaron en nosotros', 'The best proof of our work is the reviews from those who already trusted us'),
    ('basado en 141 opiniones de Google', 'based on 141 Google reviews'),
    ('5 estrellas', '5 stars'),
    ('4 estrellas', '4 stars'),
    ('3 estrellas', '3 stars'),
    ('Agendar Servicio Ahora', 'Schedule Service Now'),
    
    # FAQ page specific
    ('Resolvemos todas tus dudas sobre los servicios de', 'We answer all your questions about'),
    ('Si no encuentras lo que buscas, contáctanos directamente por WhatsApp', 'If you can\'t find what you\'re looking for, contact us directly on WhatsApp'),
    ('Si no encuentras lo que buscas, contactanos directamente por WhatsApp', 'If you can\'t find what you\'re looking for, contact us directly on WhatsApp'),
    ('¿Qué es GlobalPro Automotriz?', 'What is GlobalPro Automotive?'),
    ('¿Que es GlobalPro Automotriz?', 'What is GlobalPro Automotive?'),
    ('Somos un taller mecánico especializado en servicio automotriz integral y mecánico a domicilio en Santiago', 'We are an auto repair shop specializing in complete automotive service and mobile mechanics in Santiago'),
    ('Somos un taller mecanico especializado en servicio automotriz integral y mecanico a domicilio en Santiago', 'We are an auto repair shop specializing in complete automotive service and mobile mechanics in Santiago'),
    ('Contamos con técnicos profesionales especializados en motor, frenos, electricidad y más', 'We have professional technicians specialized in engines, brakes, electrical and more'),
    ('Contamos con tecnicos profesionales especializados en motor, frenos, electricidad y mas', 'We have professional technicians specialized in engines, brakes, electrical and more'),
    ('Nos encargamos de cubrir todas las necesidades de tu vehículo, tanto en nuestro taller físico en Pedro Aguirre Cerda como a domicilio en toda la Región Metropolitana', 'We cover all your vehicle needs, both at our physical shop in Pedro Aguirre Cerda and mobile service throughout the Metropolitan Region'),
    ('Nos encargamos de cubrir todas las necesidades de tu vehiculo, tanto en nuestro taller fisico en Pedro Aguirre Cerda como a domicilio en toda la Region Metropolitana', 'We cover all your vehicle needs, both at our physical shop in Pedro Aguirre Cerda and mobile service throughout the Metropolitan Region'),
    ('¿Cómo funciona el servicio?', 'How does the service work?'),
    ('¿Como funciona el servicio?', 'How does the service work?'),
    ('Escoge el servicio que necesitas y contáctanos por nuestra página web o por WhatsApp con nuestros asesores', 'Choose the service you need and contact us through our website or WhatsApp with our advisors'),
    ('Escoge el servicio que necesitas y contactanos por nuestra pagina web o por WhatsApp con nuestros asesores', 'Choose the service you need and contact us through our website or WhatsApp with our advisors'),
    ('Una vez agendado, el técnico irá a donde le indiques para realizar el servicio', 'Once scheduled, the technician will go where you indicate to perform the service'),
    ('Una vez agendado, el tecnico ira a donde le indiques para realizar el servicio', 'Once scheduled, the technician will go where you indicate to perform the service'),
    ('Si prefieres traer tu vehículo, puedes visitar nuestro taller en Av. Padre Alberto Hurtado 3598, Pedro Aguirre Cerda', 'If you prefer to bring your vehicle, you can visit our shop at Av. Padre Alberto Hurtado 3598, Pedro Aguirre Cerda'),
    ('Si prefieres traer tu vehiculo, puedes visitar nuestro taller en Av. Padre Alberto Hurtado 3598, Pedro Aguirre Cerda', 'If you prefer to bring your vehicle, you can visit our shop at Av. Padre Alberto Hurtado 3598, Pedro Aguirre Cerda'),
    ('¿Qué servicios ofrecen?', 'What services do you offer?'),
    ('¿Que servicios ofrecen?', 'What services do you offer?'),
    ('Nuestros técnicos están calificados para todo tipo de trabajos automotrices', 'Our technicians are qualified for all types of automotive work'),
    ('Nuestros tecnicos estan calificados para todo tipo de trabajos automotrices', 'Our technicians are qualified for all types of automotive work'),
    ('escáner y diagnóstico computarizado', 'scanner and computerized diagnostics'),
    ('scanner y diagnostico computarizado', 'scanner and computerized diagnostics'),
    ('revisión pre-compra', 'pre-purchase inspection'),
    ('revision pre-compra', 'pre-purchase inspection'),
    ('cambio de aceite de motor', 'engine oil change'),
    ('reparación de frenos', 'brake repair'),
    ('reparacion de frenos', 'brake repair'),
    ('suspensión y dirección', 'suspension and steering'),
    ('suspension y direccion', 'suspension and steering'),
    ('sistema eléctrico', 'electrical system'),
    ('sistema electrico', 'electrical system'),
    ('aire acondicionado', 'air conditioning'),
    ('cambios de embrague', 'clutch replacement'),
    ('reparaciones complejas', 'complex repairs'),
    ('Trabajamos tanto a domicilio como en nuestro taller', 'We work both mobile and at our shop'),
    ('¿Los servicios cuentan con garantía?', 'Do services come with a warranty?'),
    ('¿Los servicios cuentan con garantia?', 'Do services come with a warranty?'),
    ('Sí. En GlobalPro Automotriz ofrecemos garantía en todos nuestros servicios', 'Yes. At GlobalPro Automotive we offer a warranty on all our services'),
    ('Si. En GlobalPro Automotriz ofrecemos garantia en todos nuestros servicios', 'Yes. At GlobalPro Automotive we offer a warranty on all our services'),
    ('Los periodos de garantía varían entre 3, 6 y 12 meses dependiendo del tipo de servicio realizado', 'Warranty periods vary between 3, 6 and 12 months depending on the type of service performed'),
    ('Los periodos de garantia varian entre 3, 6 y 12 meses dependiendo del tipo de servicio realizado', 'Warranty periods vary between 3, 6 and 12 months depending on the type of service performed'),
    ('¿Entregan información de todo lo que hace el técnico en la reparación?', 'Do you provide information about everything the technician does during the repair?'),
    ('¿Entregan informacion de todo lo que hace el tecnico en la reparacion?', 'Do you provide information about everything the technician does during the repair?'),
    ('Cada técnico está capacitado para entregar seriedad, transparencia y estructura a cada información que se recupere del vehículo mediante el escáner de diagnóstico', 'Each technician is trained to provide seriousness, transparency and structure to all information recovered from the vehicle through the diagnostic scanner'),
    ('Cada tecnico esta capacitado para entregar seriedad, transparencia y estructura a cada informacion que se recupere del vehiculo mediante el escaner de diagnostico', 'Each technician is trained to provide seriousness, transparency and structure to all information recovered from the vehicle through the diagnostic scanner'),
    ('Además, entregamos un informe detallado de todas las intervenciones realizadas', 'Additionally, we provide a detailed report of all interventions performed'),
    ('Ademas, entregamos un informe detallado de todas las intervenciones realizadas', 'Additionally, we provide a detailed report of all interventions performed'),
    ('¿Los servicios incluyen repuestos?', 'Do services include parts?'),
    ('Cada servicio tiene un costo base de mano de obra sin repuesto añadido, así evitamos la especulación de precios por cada pieza', 'Each service has a base labor cost with no parts added, so we avoid price speculation on each part'),
    ('Cada servicio tiene un costo base de mano de obra sin repuesto anadido, asi evitamos la especulacion de precios por cada pieza', 'Each service has a base labor cost with no parts added, so we avoid price speculation on each part'),
    ('Te recomendaremos siempre las mejores casas de repuesto para tu auto', 'We will always recommend the best parts suppliers for your car'),
    ('¿Qué métodos de pago aceptan?', 'What payment methods do you accept?'),
    ('¿Que metodos de pago aceptan?', 'What payment methods do you accept?'),
    ('Puedes cancelar con efectivo, transferencia electrónica, o tarjetas de crédito, débito y prepago a través de nuestros sistemas de pago', 'You can pay with cash, electronic transfer, or credit, debit and prepaid cards through our payment systems'),
    ('Puedes cancelar con efectivo, transferencia electronica, o tarjetas de credito, debito y prepago a traves de nuestros sistemas de pago', 'You can pay with cash, electronic transfer, or credit, debit and prepaid cards through our payment systems'),
    ('Consulta con nuestros asesores las opciones disponibles al momento de agendar', 'Check with our advisors for available options when scheduling'),
    ('¿Puedo reagendar el servicio?', 'Can I reschedule the service?'),
    ('¿Puedo reagendar el servicio?', 'Can I reschedule the service?'),
    ('Sí, puedes reagendar el servicio comunicándote con nuestros asesores vía WhatsApp o llamando al', 'Yes, you can reschedule the service by contacting our advisors via WhatsApp or calling'),
    ('Si, puedes reagendar el servicio comunicandote con nuestros asesores via WhatsApp o llamando al', 'Yes, you can reschedule the service by contacting our advisors via WhatsApp or calling'),
    ('con antelación para reprogramar tu cita', 'in advance to reschedule your appointment'),
    ('con antelacion para reprogramar tu cita', 'in advance to reschedule your appointment'),
    ('¿Cuál es la política de cancelación del servicio?', 'What is the service cancellation policy?'),
    ('¿Cual es la politica de cancelacion del servicio?', 'What is the service cancellation policy?'),
    ('Si necesitas cancelar o reagendar, te pedimos hacerlo con al menos 3 horas de anticipación para no afectar la programación de nuestros técnicos', 'If you need to cancel or reschedule, please do so at least 3 hours in advance to avoid affecting our technicians\' schedule'),
    ('Si necesitas cancelar o reagendar, te pedimos hacerlo con al menos 3 horas de anticipacion para no afectar la programacion de nuestros tecnicos', 'If you need to cancel or reschedule, please do so at least 3 hours in advance to avoid affecting our technicians\' schedule'),
    ('En caso de cancelaciones tardías, se podrá retener un monto por gastos logísticos', 'In case of late cancellations, an amount may be retained for logistical expenses'),
    ('En caso de cancelaciones tardias, se podra retener un monto por gastos logisticos', 'In case of late cancellations, an amount may be retained for logistical expenses'),
    ('Consulta nuestros términos y condiciones para más detalle', 'Check our terms and conditions for more details'),
    ('Consulta nuestros terminos y condiciones para mas detalle', 'Check our terms and conditions for more details'),
    ('¿Cuánto se demora el reembolso en caso de cancelación?', 'How long does a cancellation refund take?'),
    ('¿Cuanto se demora el reembolso en caso de cancelacion?', 'How long does a cancellation refund take?'),
    ('Los reembolsos se procesan en menos de 48 horas en días hábiles, dependiendo del método de pago utilizado', 'Refunds are processed within 48 business hours, depending on the payment method used'),
    ('Los reembolsos se procesan en menos de 48 horas en dias habiles, dependiendo del metodo de pago utilizado', 'Refunds are processed within 48 business hours, depending on the payment method used'),
    ('Para más información, comunícate directamente con nuestros asesores', 'For more information, contact our advisors directly'),
    ('Para mas informacion, comunicate directamente con nuestros asesores', 'For more information, contact our advisors directly'),
    ('¿Tienes más preguntas?', 'Have more questions?'),
    ('Nuestro equipo de asesores está listo para ayudarte', 'Our team of advisors is ready to help you'),
    ('Nuestro equipo de asesores esta listo para ayudarte', 'Our team of advisors is ready to help you'),
    ('Escríbenos por WhatsApp y resuelve todas tus dudas sobre nuestros servicios automotrices en Santiago', 'Message us on WhatsApp and resolve all your questions about our automotive services in Santiago'),
    ('Escribenos por WhatsApp y resuelve todas tus dudas sobre nuestros servicios automotrices en Santiago', 'Message us on WhatsApp and resolve all your questions about our automotive services in Santiago'),
    
    # 404 page
    ('Página no encontrada', 'Page Not Found'),
    ('Pagina no encontrada', 'Page Not Found'),
    ('Lo sentimos, la página que buscas no existe', 'Sorry, the page you are looking for does not exist'),
    ('Lo sentimos, la pagina que buscas no existe', 'Sorry, the page you are looking for does not exist'),
    ('Volver al Inicio', 'Back to Home'),
    
    # Privacy policy
    ('Política de Privacidad', 'Privacy Policy'),
    ('Politica de Privacidad', 'Privacy Policy'),
    
    # Mechanical inspection
    ('Inspección Mecánica', 'Mechanical Inspection'),
    ('Inspeccion Mecanica', 'Mechanical Inspection'),
    
    # Services at home
    ('Servicios a Domicilio', 'Services at Home'),
    ('Servicios Domicilio', 'Services at Home'),
    
    # Vehiculos page
    ('Vehículos que Atendemos', 'Vehicles We Service'),
    ('Vehiculos que Atendemos', 'Vehicles We Service'),
    ('Selecciona tu vehículo para ver los servicios disponibles', 'Select your vehicle to see available services'),
    ('Selecciona tu vehiculo para ver los servicios disponibles', 'Select your vehicle to see available services'),
    ('Haz clic en la foto para ampliarla', 'Click the photo to enlarge'),
    ('Haz clic en la foto para ampliarla', 'Click the photo to enlarge'),
    
    # Service page specific terms
    ('Cambio de Aceite a Domicilio', 'Oil Change at Home'),
    ('Cambio de Frenos a Domicilio', 'Brake Repair at Home'),
    ('Diagnóstico con Scanner a Domicilio', 'Diagnostic Scan at Home'),
    ('Diagnostico con Scanner a Domicilio', 'Diagnostic Scan at Home'),
    ('Electricidad Automotriz a Domicilio', 'Auto Electrical at Home'),
    ('Aire Acondicionado Automotriz', 'Automotive Air Conditioning'),
    ('Mecánico 24 Horas', '24-Hour Mechanic'),
    ('Mecanico 24 Horas', '24-Hour Mechanic'),
    ('Mecánico de Emergencia', 'Emergency Mechanic'),
    ('Mecanico de Emergencia', 'Emergency Mechanic'),
]

# ============================================================
# COMUNA-SPECIFIC FAQ TRANSLATIONS
# ============================================================
COMUNA_FAQ = {
    'q1_title': 'Looking for a mobile mechanic in {comuna}?',
    'q1_answer': 'At GlobalPro Automotive, we are the immediate response. Whether you\'re at home, at the office, or stranded on the street in {comuna}, our mobile mechanic service covers the entire Metropolitan Region with speed and professionalism. We bring the auto repair shop to your location so you don\'t waste time or money on tow trucks.',
    'q2_title': 'How long does it take to get to {comuna}?',
    'q2_answer': 'In most cases, we serve you within 24 hours. Our 24/7 emergency service can arrive the same day in {comuna}. Our technicians have high availability to cover your area.',
    'q3_title': 'What mechanic services do you offer in {comuna}?',
    'q3_answer': 'We offer general mechanics, brake repair, clutch, auto electrical, air conditioning, diagnostic scanner, oil change, alignment, suspension, battery service, spark plugs, timing belt, preventive maintenance, and 24/7 emergencies — all at your doorstep in {comuna}.',
    'q4_title': 'Do you handle mechanical emergencies in {comuna} 24 hours?',
    'q4_answer': 'Yes, GlobalPro offers 24/7 mechanical emergency service in {comuna}. If your car won\'t start, has a breakdown on the road, or needs immediate assistance, call or message us on WhatsApp and a technician will be with you in under 60 minutes.',
    'q5_title': 'What vehicles do you service in {comuna}?',
    'q5_answer': 'We service compact sedans, SUVs, family vehicles, and all brands: Toyota, Hyundai, Kia, Chevrolet, Nissan, Renault, Peugeot, Ford, Volkswagen, Honda, Mazda, Suzuki, Subaru, Fiat, MG, and more. Our technicians travel to {comuna} with specialized tools for each type of vehicle.',
}

# ============================================================
# SEO PARAGRAPHS FOR COMUNAS
# ============================================================
def comuna_seo_p1(comuna):
    return f'Looking for a <strong>mobile mechanic in {comuna}</strong>? At <strong>GlobalPro Automotive</strong>, we understand that residents of <strong>{comuna}</strong> need fast and reliable solutions for their vehicle maintenance. Our team of certified technicians comes directly to your home, office, or location in <strong>{comuna}</strong>, bringing state-of-the-art diagnostic tools and quality replacement parts to solve any mechanical problem without you having to move.'

def comuna_seo_p2(comuna):
    return f'Whether you need an <strong>oil change</strong>, <strong>brake repair</strong>, <strong>computer diagnostics</strong>, or a <strong>24/7 emergency service</strong>, at GlobalPro we have the experience and commitment to serve you in <strong>{comuna}</strong> with the same quality as a formal shop but with the convenience of being at your own doorstep. We are proud to be the most reliable <strong>mobile mechanic</strong> service in the Metropolitan Region, with over 5,000 satisfied customers who recommend us.'

def comuna_seo_p3(comuna):
    return f'<strong>{comuna}</strong> is one of the areas with the highest demand, which is why we have optimized our response times so a technician can be with you faster than you think. If your car won\'t start, you have an electrical system failure, or simply need your <strong>preventive maintenance</strong> up to date, our <strong>mobile mechanic in {comuna}</strong> is the solution. Contact us on WhatsApp and schedule your appointment today.'

# ============================================================
# CANONICAL AND HREFLANG
# ============================================================
SERVICE_SLUG_MAP = {
    'aire-acondicionado-automotriz': 'air-conditioning',
    'cambio-de-aceite-a-domicilio': 'oil-change-at-home',
    'cambio-de-frenos-a-domicilio': 'brake-repair-at-home',
    'diagnostico-con-scanner-a-domicilio': 'diagnostic-scan-at-home',
    'electricidad-automotriz-a-domicilio': 'auto-electrical-at-home',
    'mecanico-24-horas': '24-hour-mechanic',
    'mecanico-de-emergencia': 'emergency-mechanic',
}

OTHER_SLUG_MAP = {
    'contacto': 'contacto',
    'faq': 'faq',
    'quienes-somos': 'about-us',
    'politica-privacidad': 'privacy-policy',
    'inspeccion-mecanica': 'mechanical-inspection',
    'servicios-domicilio': 'services-at-home',
}

# ============================================================
# COMUNA NAME MAPPING (slug -> display name)
# ============================================================
COMUNA_NAMES = {
    'alhue': 'Alhué', 'buin': 'Buín', 'calera-de-tango': 'Calera de Tango',
    'cerrillos': 'Cerrillos', 'cerro-navia': 'Cerro Navia', 'colina': 'Colina',
    'conchali': 'Conchalí', 'curacavi': 'Curacaví', 'el-bosque': 'El Bosque',
    'el-monte': 'El Monte', 'estacion-central': 'Estación Central',
    'huechuraba': 'Huechuraba', 'independencia': 'Independencia',
    'isla-de-maipo': 'Isla de Maipo', 'la-cisterna': 'La Cisterna',
    'la-florida': 'La Florida', 'la-granja': 'La Granja', 'la-pintana': 'La Pintana',
    'la-reina': 'La Reina', 'lampa': 'Lampa', 'las-condes': 'Las Condes',
    'lo-barnechea': 'Lo Barnechea', 'lo-espejo': 'Lo Espejo', 'lo-prado': 'Lo Prado',
    'macul': 'Macul', 'maipu': 'Maipú', 'maria-pinto': 'María Pinto',
    'melipilla': 'Melipilla', 'nunoa': 'Ñuñoa', 'padre-hurtado': 'Padre Hurtado',
    'paine': 'Paine', 'pedro-aguirre-cerda': 'Pedro Aguirre Cerda',
    'penaflor': 'Peñaflor', 'penalolen': 'Peñalolén', 'pirque': 'Pirque',
    'providencia': 'Providencia', 'pudahuel': 'Pudahuel', 'puente-alto': 'Puente Alto',
    'quilicura': 'Quilicura', 'quinta-normal': 'Quinta Normal', 'recoleta': 'Recoleta',
    'renca': 'Renca', 'san-bernardo': 'San Bernardo', 'san-joaquin': 'San Joaquín',
    'san-jose-de-maipo': 'San José de Maipo', 'san-miguel': 'San Miguel',
    'san-pedro': 'San Pedro', 'san-ramon': 'San Ramón', 'santiago': 'Santiago',
    'talagante': 'Talagante', 'tiltil': 'Tiltil', 'vitacura': 'Vitacura',
}

# ============================================================
# DETAILED SERVICE BLOCKS FOR COMUNAS (10 blocks)
# ============================================================
def get_detailed_service_blocks(comuna):
    """Generate the 10 detailed service blocks for a comuna page"""
    c = comuna
    blocks = [
        {
            'icon': 'fa-house-chimney-medical',
            'title': f'Mobile Mechanic in {c}',
            'text': f'GlobalPro Automotive brings the auto repair shop right to your doorstep in {c}, western Santiago. No need to waste time on trips or waiting at shops: our certified technicians arrive with professional diagnostic tools and quality parts to service compact sedans, SUVs, and family vehicles directly at your home. We cover the neighborhoods of {c} center and surrounding areas to offer you fast and reliable service, with no hidden costs or surprises. Schedule on WhatsApp and receive personalized attention.'
        },
        {
            'icon': 'fa-barcode',
            'title': f'Automotive Diagnostics in {c}',
            'text': f'Automotive diagnostics is the key tool for an accurate diagnosis with no guesswork. At GlobalPro, we perform complete electronic scans in {c} to detect faults in sensors, ECU modules, injection systems, ABS, airbags and more. Vehicles driving through western Santiago face traffic and weather conditions that generate specific error codes. Our technicians interpret each code and offer real solutions to get your car running like new again, right at your location.'
        },
        {
            'icon': 'fa-compact-disc',
            'title': f'Brakes & Pads in {c}',
            'text': f'Your family\'s safety depends on the condition of your brakes. At GlobalPro we inspect pads, rotors, calipers, brake lines and hydraulic fluid directly in {c}. Frequent traffic on highways and main roads accelerates wear on braking components. Our service includes digital measurement of pad thickness, diagnosis of braking vibrations, and replacement with high-specification components. Don\'t take risks: schedule your brake inspection at home in {c} today.'
        },
        {
            'icon': 'fa-oil-can',
            'title': f'Oil Change in {c}',
            'text': f'Regular oil changes are the most important investment to protect your vehicle\'s engine. GlobalPro performs this service at home in {c} with premium synthetic and semi-synthetic oils from brands like Castrol, Mobil, and Shell. We include oil filter, air filter inspection, and fluid level check. For compact sedans, SUVs, and family vehicles driving through western Santiago, urban driving conditions require change intervals between 5,000 and 10,000 km. Schedule quickly on WhatsApp.'
        },
        {
            'icon': 'fa-road',
            'title': f'Alignment & Suspension in {c}',
            'text': f'The streets and avenues of {c} can affect your vehicle\'s alignment and suspension. Potholes, speed bumps, and road irregularities cause wear on shock absorbers, ball joints, tie rod ends, and bushings. GlobalPro performs computerized alignment and complete suspension inspection at home in {c}. We detect steering wheel vibrations, uneven tire wear, and misalignment with precision equipment, restoring stability and safety to your vehicle without you having to leave home.'
        },
        {
            'icon': 'fa-gears',
            'title': f'Engine Repair in {c}',
            'text': f'When your vehicle experiences power loss, excessive oil consumption, exhaust smoke, or abnormal noises, you may need a thorough engine inspection. At GlobalPro, we service compact sedans, SUVs, and family vehicles in {c} with advanced diagnostics including compression and pre-compression testing to evaluate the internal condition of cylinders, pistons, and rings. Our mechanics resolve everything from minor high-mileage issues like valve cover gaskets to major block repairs.'
        },
        {
            'icon': 'fa-sync-alt',
            'title': f'Clutch & Timing Belt in {c}',
            'text': f'The clutch and timing belt are critical components that cannot fail. A worn clutch makes gear shifting difficult, while a broken belt can irreversibly damage the engine. GlobalPro handles mechanical emergencies in {c} to replace these components with complete OEM-quality kits. We service compact sedans, SUVs, and family vehicles with certified parts, guaranteeing professional work without having to tow your vehicle to a shop.'
        },
        {
            'icon': 'fa-car-battery',
            'title': f'Battery & Electrical Service in {c}',
            'text': f'If your vehicle won\'t start, the lights look dim, or you hear a click when turning the key, the problem could be the battery or electrical system. At GlobalPro we perform complete auto electrical diagnostics at home in {c}: we measure battery charge, test the alternator, verify the starter motor, and inspect wiring. Temperature changes in the Santiago area directly affect battery life. We respond to 24/7 emergencies so you don\'t get stranded.'
        },
        {
            'icon': 'fa-clipboard-check',
            'title': f'Spark Plug Replacement & Maintenance in {c}',
            'text': f'Worn spark plugs increase fuel consumption and reduce your vehicle\'s power. At GlobalPro, we replace spark plugs to the manufacturer\'s exact specifications at home in {c}. We complement this with a preventive home maintenance plan that includes inspection of filters, oils, brake fluid, antifreeze, and belts. A well-maintained vehicle lasts longer and avoids costly repairs. Schedule your preventive maintenance in {c}.'
        },
        {
            'icon': 'fa-truck-medical',
            'title': f'24/7 Emergencies & Auto Repair Shop Near Me',
            'text': f'If your vehicle breaks down in {c} or you suffer a mechanical emergency in the Santiago area, GlobalPro responds 24 hours a day. We are the closest mobile auto repair shop to you: we arrive in under 60 minutes for emergencies. From dead batteries to engine failures, our technicians offer immediate solutions in {c} center and surrounding areas. No matter the time or place: GlobalPro is your trusted mechanic in {c} for any automotive emergency.'
        },
    ]
    return blocks

# ============================================================
# APPLY REPLACEMENTS
# ============================================================
def apply_replacements(html, extra_replacements=None):
    """Apply all text replacements to HTML content"""
    replacements = list(GLOBAL_REPLACEMENTS)
    if extra_replacements:
        replacements.extend(extra_replacements)
    
    for old, new in replacements:
        html = html.replace(old, new)
    
    return html

# ============================================================
# FIX JSON-LD STRUCTURED DATA
# ============================================================
def fix_jsonld(html, page_type, comuna=None, service_name=None):
    """Translate JSON-LD structured data in the HTML"""
    # Fix LocalBusiness name
    html = html.replace('GlobalPro Taller Mecánico', 'GlobalPro Auto Repair')
    html = html.replace('GlobalPro Taller Mecanico', 'GlobalPro Auto Repair')
    html = html.replace('GLOBAL PRO Automotriz', 'GlobalPro Automotive')
    html = html.replace('GlobalPro Automotriz', 'GlobalPro Automotive')
    
    # Fix BreadcrumbList
    html = html.replace('"name": "Inicio"', '"name": "Home"')
    html = html.replace('"name": "Comunas"', '"name": "Areas"')
    html = html.replace('"name": "Servicios"', '"name": "Services"')
    html = html.replace('"name": "Quienes Somos"', '"name": "About Us"')
    html = html.replace('"name": "Cambio de Aceite a Domicilio"', '"name": "Oil Change at Home"')
    html = html.replace('"name": "Cambio de Frenos a Domicilio"', '"name": "Brake Repair at Home"')
    html = html.replace('"name": "Diagnostico con Scanner a Domicilio"', '"name": "Diagnostic Scan at Home"')
    html = html.replace('"name": "Electricidad Automotriz a Domicilio"', '"name": "Auto Electrical at Home"')
    html = html.replace('"name": "Aire Acondicionado Automotriz"', '"name": "Air Conditioning"')
    html = html.replace('"name": "Mecanico 24 Horas"', '"name": "24-Hour Mechanic"')
    html = html.replace('"name": "Mecanico de Emergencia"', '"name": "Emergency Mechanic"')
    
    # Fix Service type
    html = html.replace('"serviceType": "Mecanico a Domicilio"', '"serviceType": "Mobile Mechanic"')
    html = html.replace('"serviceType": "Cambio de Aceite a Domicilio"', '"serviceType": "Oil Change at Home"')
    
    # Fix HowTo
    html = html.replace('"name": "Como verificar el estado de tu vehiculo', '"name": "How to check your vehicle')
    html = html.replace('"name": "Como realizar un cambio de aceite', '"name": "How to perform an oil change')
    html = html.replace('"description": "Guia de diagnostico basico', '"description": "Basic diagnostic guide')
    html = html.replace('"description": "Guia paso a paso', '"description": "Step-by-step guide')
    html = html.replace('"name": "Revision visual"', '"name": "Visual inspection"')
    html = html.replace('"name": "Niveles de liquidos"', '"name": "Fluid levels"')
    html = html.replace('"name": "Bateria"', '"name": "Battery"')
    html = html.replace('"name": "Contacta a GlobalPro"', '"name": "Contact GlobalPro"')
    html = html.replace('"name": "Cotiza por WhatsApp"', '"name": "Get a Quote on WhatsApp"')
    html = html.replace('"name": "Agenda tu cita"', '"name": "Schedule your appointment"')
    html = html.replace('"name": "Drenaje del aceite usado"', '"name": "Drain used oil"')
    html = html.replace('"name": "Filtro y aceite nuevo"', '"name": "New filter and oil"')
    
    # Fix ContactPage
    html = html.replace('"@type": "ContactPage"', '"@type": "ContactPage"')
    html = html.replace('"name": "Contacto - GlobalPro Automotriz"', '"name": "Contact - GlobalPro Automotive"')
    html = html.replace('"description": "Página de contacto de GlobalPro Automotriz', '"description": "Contact page for GlobalPro Automotive')
    
    # Fix FAQ JSON-LD for comunas
    if comuna:
        c = comuna
        # Fix FAQ questions in JSON-LD
        html = re.sub(
            r'"name":\s*"¿Cuanto cuesta el mecanico a domicilio en [^"]*?"',
            f'"name": "How much does a mobile mechanic cost in {c}?"',
            html
        )
        html = re.sub(
            r'"name":\s*"¿Cuanto demoran en llegar a [^"]*?"',
            f'"name": "How long does it take to get to {c}?"',
            html
        )
        html = re.sub(
            r'"name":\s*"¿Que servicios de mecanica ofrecen en [^"]*?"',
            f'"name": "What mechanic services do you offer in {c}?"',
            html
        )
        html = re.sub(
            r'"name":\s*"¿Atienden emergencias mecanicas en [^"]*? las 24 horas\\?"',
            f'"name": "Do you handle mechanical emergencies in {c} 24 hours?"',
            html
        )
        html = re.sub(
            r'"name":\s*"¿Que vehiculos atienden en [^"]*?"',
            f'"name": "What vehicles do you service in {c}?"',
            html
        )
    
    return html

# ============================================================
# FIX CANONICAL AND HREFLANG TAGS
# ============================================================
def fix_canonical_hreflang(html, en_path):
    """Fix canonical URLs and hreflang tags for English pages"""
    base_url = 'https://mecanico247.com'
    es_path = en_path.replace('/en/', '/').replace('/air-conditioning', '/aire-acondicionado-automotriz').replace('/oil-change-at-home', '/cambio-de-aceite-a-domicilio').replace('/brake-repair-at-home', '/cambio-de-frenos-a-domicilio').replace('/diagnostic-scan-at-home', '/diagnostico-con-scanner-a-domicilio').replace('/auto-electrical-at-home', '/electricidad-automotriz-a-domicilio').replace('/24-hour-mechanic', '/mecanico-24-horas').replace('/emergency-mechanic', '/mecanico-de-emergencia').replace('/about-us', '/quienes-somos').replace('/privacy-policy', '/politica-privacidad').replace('/mechanical-inspection', '/inspeccion-mecanica').replace('/services-at-home', '/servicios-domicilio')
    
    en_url = base_url + en_path
    es_url = base_url + es_path
    
    # Remove existing hreflang tags
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^/]*/>', '', html)
    
    # Fix canonical
    html = re.sub(r'<link rel="canonical"[^/]*/>', f'<link rel="canonical" href="{en_url}"/>', html)
    
    # Fix og:url
    html = re.sub(r'<meta property="og:url"[^/]*/>', f'<meta property="og:url" content="{en_url}"/>', html)
    
    # Add hreflang tags before </head>
    hreflang = f'''<link rel="alternate" hreflang="es" href="{es_url}" />
<link rel="alternate" hreflang="en" href="{en_url}" />
<link rel="alternate" hreflang="x-default" href="{es_url}" />'''
    
    html = html.replace('</head>', hreflang + '\n</head>')
    
    return html

# ============================================================
# ADD LANGUAGE SWITCHER
# ============================================================
def add_lang_switcher(html, en_path):
    """Add language switcher to the page"""
    # Remove any existing lang-switcher div
    html = re.sub(r'<div id="lang-switcher"[^>]*>.*?</div>\s*(<script>.*?</script>)?\s*', '', html, flags=re.DOTALL)
    
    # Calculate ES path
    es_path = en_path.replace('/en/', '/').replace('/air-conditioning', '/aire-acondicionado-automotriz').replace('/oil-change-at-home', '/cambio-de-aceite-a-domicilio').replace('/brake-repair-at-home', '/cambio-de-frenos-a-domicilio').replace('/diagnostic-scan-at-home', '/diagnostico-con-scanner-a-domicilio').replace('/auto-electrical-at-home', '/electricidad-automotriz-a-domicilio').replace('/24-hour-mechanic', '/mecanico-24-horas').replace('/emergency-mechanic', '/mecanico-de-emergencia').replace('/about-us', '/quienes-somos').replace('/privacy-policy', '/politica-privacidad').replace('/mechanical-inspection', '/inspeccion-mecanica').replace('/services-at-home', '/servicios-domicilio')
    
    switcher = f'''<div id="lang-switcher" style="position:fixed; top:80px; right:15px; z-index:9999; display:flex; gap:4px;">
  <a href="{es_path}" style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; text-decoration:none;">🇪🇸 ES</a>
  <span style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700;">🇬🇧 EN</span>
</div>'''
    
    # Add before </body>
    html = html.replace('</body>', switcher + '\n</body>')
    
    # Add language detection script
    lang_detect = '''<script>
// Language detection for English pages
(function() {
  if (sessionStorage.getItem('lang_choice')) return;
  sessionStorage.setItem('lang_choice', 'en');
})();
</script>'''
    html = html.replace('</body>', lang_detect + '\n</body>')
    
    return html

# ============================================================
# FIX URLS IN NAVIGATION FOR ENGLISH PAGES
# ============================================================
def fix_nav_urls(html):
    """Fix navigation URLs for English pages"""
    # Service dropdown URLs
    for es_slug, en_slug in SERVICE_SLUG_MAP.items():
        html = html.replace(f'href="/servicios/{es_slug}"', f'href="/en/servicios/{en_slug}"')
        html = html.replace(f'href="/servicios/{es_slug}/"', f'href="/en/servicios/{en_slug}/"')
    
    # Comuna dropdown URLs
    for slug in COMUNA_NAMES:
        html = html.replace(f'href="/comunas/{slug}"', f'href="/en/comunas/{slug}"')
    
    # Other page URLs
    html = html.replace('href="/quienes-somos"', 'href="/en/about-us"')
    html = html.replace('href="/contacto"', 'href="/en/contacto"')
    html = html.replace('href="/faq"', 'href="/en/faq"')
    html = html.replace('href="/politica-privacidad"', 'href="/en/privacy-policy"')
    html = html.replace('href="/inspeccion-mecanica"', 'href="/en/mechanical-inspection"')
    html = html.replace('href="/servicios-domicilio"', 'href="/en/services-at-home"')
    html = html.replace('href="/blog/"', 'href="/en/blog/"')
    html = html.replace('href="/vehiculos/"', 'href="/en/vehiculos/"')
    html = html.replace('href="/vehiculos"', 'href="/en/vehiculos"')
    html = html.replace('href="/marcas_automotrices/"', 'href="/en/marcas_automotrices/"')
    html = html.replace('href="/marcas_automotrices"', 'href="/en/marcas_automotrices"')
    
    # Home link
    html = html.replace('href="/"', 'href="/en/"')
    html = html.replace('href="#mecanico-domicilio-seo"', 'href="/en/#mecanico-domicilio-seo"')
    html = html.replace('href="#servicios"', 'href="/en/#servicios"')
    html = html.replace('href="#inicio"', 'href="/en/#inicio"')
    
    return html

# ============================================================
# PROCESS COMUNA PAGES
# ============================================================
def process_comunas():
    """Process all 52 comuna pages"""
    print("\n=== Step 2: Processing comuna pages ===")
    count = 0
    
    for slug, name in COMUNA_NAMES.items():
        es_file = os.path.join(BASE, 'comunas', f'{slug}.html')
        en_file = os.path.join(EN_BASE, 'comunas', f'{slug}.html')
        
        if not os.path.exists(es_file):
            print(f"  WARNING: Missing {es_file}")
            continue
        
        with open(es_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Apply global replacements
        html = apply_replacements(html)
        
        # Fix SEO paragraphs - replace the Spanish ones with English
        # P1
        p1_es_pattern = r'Buscando un <strong>mecánico a domicilio en [^<]*</strong>\? En <strong>GlobalPro Automotriz</strong> entendemos.*?sin que tengas que moverte\.'
        p1_es_pattern2 = r'Buscando un <strong>mecanico a domicilio en [^<]*</strong>\? En <strong>GlobalPro Automotriz</strong> entendemos.*?sin que tengas que moverte\.'
        html = re.sub(p1_es_pattern, comuna_seo_p1(name), html, flags=re.DOTALL)
        html = re.sub(p1_es_pattern2, comuna_seo_p1(name), html, flags=re.DOTALL)
        
        # P2
        p2_es_pattern = r'Ya sea que necesites un <strong>cambio de aceite</strong>.*?que nos recomiendan\.'
        p2_es_pattern2 = r'Ya sea que necesites un <strong>cambio de aceite</strong>.*?que nos recomiendan\.'
        html = re.sub(p2_es_pattern, comuna_seo_p2(name), html, flags=re.DOTALL)
        html = re.sub(p2_es_pattern2, comuna_seo_p2(name), html, flags=re.DOTALL)
        
        # P3
        p3_es_pattern = r'<strong>[^<]*</strong> es una de las comunas donde mayor demanda tenemos.*?agenda tu cita hoy mismo\.'
        p3_es_pattern2 = r'<strong>[^<]*</strong> es una de las comunas donde mayor demanda tenemos.*?agenda tu cita hoy mismo\.'
        html = re.sub(p3_es_pattern, comuna_seo_p3(name), html, flags=re.DOTALL)
        html = re.sub(p3_es_pattern2, comuna_seo_p3(name), html, flags=re.DOTALL)
        
        # Fix FAQ section in HTML body for comunas
        # Replace FAQ questions/answers with English versions
        faq_replacements = [
            (f'¿Cuanto cuesta el mecanico a domicilio en {name}?',
             COMUNA_FAQ['q1_title'].format(comuna=name)),
            (f'¿Cuanto demoran en llegar a {name}?',
             COMUNA_FAQ['q2_title'].format(comuna=name)),
            (f'¿Que servicios de mecanica ofrecen en {name}?',
             COMUNA_FAQ['q3_title'].format(comuna=name)),
            (f'¿Atienden emergencias mecanicas en {name} las 24 horas?',
             COMUNA_FAQ['q4_title'].format(comuna=name)),
            (f'¿Que vehiculos atienden en {name}?',
             COMUNA_FAQ['q5_title'].format(comuna=name)),
        ]
        
        for old, new in faq_replacements:
            html = html.replace(old, new)
        
        # Fix FAQ answers - these are longer text blocks
        # Q1 answer
        q1_answer_old = r'El costo depende del servicio solicitado.*?Cotiza sin compromiso por WhatsApp con GlobalPro y recibe un presupuesto transparente a domicilio en [^<]*\.'
        html = re.sub(q1_answer_old, COMUNA_FAQ['q1_answer'].format(comuna=name), html, flags=re.DOTALL)
        
        # Fix JSON-LD
        html = fix_jsonld(html, 'comuna', comuna=name)
        
        # Fix canonical and hreflang
        en_path = f'/en/comunas/{slug}'
        html = fix_canonical_hreflang(html, en_path)
        
        # Fix nav URLs
        html = fix_nav_urls(html)
        
        # Add language switcher
        html = add_lang_switcher(html, en_path)
        
        # Fix title
        html = html.replace(f'en {name} | GlobalPro Automotriz - Santiago', f'in {name} | GlobalPro Automotive - Santiago')
        html = html.replace(f'en {name} | GlobalPro Auto Repair - Santiago', f'in {name} | GlobalPro Auto Repair - Santiago')
        
        # Write the English version
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        count += 1
        if count % 10 == 0:
            print(f"  Processed {count} comuna pages...")
    
    print(f"  Total comuna pages processed: {count}")
    return count

# ============================================================
# PROCESS SERVICE PAGES
# ============================================================
def process_services():
    """Process all 7 service pages"""
    print("\n=== Step 3: Processing service pages ===")
    count = 0
    
    for es_slug, en_slug in SERVICE_SLUG_MAP.items():
        es_file = os.path.join(BASE, 'servicios', f'{es_slug}.html')
        en_file = os.path.join(EN_BASE, 'servicios', f'{en_slug}.html')
        
        if not os.path.exists(es_file):
            print(f"  WARNING: Missing {es_file}")
            continue
        
        with open(es_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Apply global replacements
        html = apply_replacements(html)
        
        # Fix JSON-LD
        html = fix_jsonld(html, 'service')
        
        # Fix canonical and hreflang
        en_path = f'/en/servicios/{en_slug}'
        html = fix_canonical_hreflang(html, en_path)
        
        # Fix nav URLs
        html = fix_nav_urls(html)
        
        # Add language switcher
        html = add_lang_switcher(html, en_path)
        
        # Write the English version
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        count += 1
        print(f"  Processed: {es_slug} -> {en_slug}")
    
    print(f"  Total service pages processed: {count}")
    return count

# ============================================================
# PROCESS VEHICLE PAGES
# ============================================================
def process_vehicles():
    """Process all vehicle pages"""
    print("\n=== Step 4: Processing vehicle pages ===")
    count = 0
    
    veh_dir = os.path.join(BASE, 'vehiculos')
    en_veh_dir = os.path.join(EN_BASE, 'vehiculos')
    
    for filename in os.listdir(veh_dir):
        if not filename.endswith('.html'):
            continue
        
        es_file = os.path.join(veh_dir, filename)
        en_file = os.path.join(en_veh_dir, filename)
        
        with open(es_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Apply global replacements
        html = apply_replacements(html)
        
        # Fix JSON-LD
        html = fix_jsonld(html, 'vehicle')
        
        # Fix canonical and hreflang
        en_path = f'/en/vehiculos/{filename}'
        html = fix_canonical_hreflang(html, en_path)
        
        # Fix nav URLs
        html = fix_nav_urls(html)
        
        # Add language switcher
        html = add_lang_switcher(html, en_path)
        
        # Write the English version
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        count += 1
    
    print(f"  Total vehicle pages processed: {count}")
    return count

# ============================================================
# PROCESS BRAND PAGES
# ============================================================
def process_brands():
    """Process all brand pages"""
    print("\n=== Step 5: Processing brand pages ===")
    count = 0
    
    brand_dir = os.path.join(BASE, 'marcas_automotrices')
    en_brand_dir = os.path.join(EN_BASE, 'marcas_automotrices')
    
    for filename in os.listdir(brand_dir):
        if not filename.endswith('.html'):
            continue
        
        es_file = os.path.join(brand_dir, filename)
        en_file = os.path.join(en_brand_dir, filename)
        
        with open(es_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Apply global replacements
        html = apply_replacements(html)
        
        # Fix JSON-LD
        html = fix_jsonld(html, 'brand')
        
        # Fix canonical and hreflang
        en_path = f'/en/marcas_automotrices/{filename}'
        html = fix_canonical_hreflang(html, en_path)
        
        # Fix nav URLs
        html = fix_nav_urls(html)
        
        # Add language switcher
        html = add_lang_switcher(html, en_path)
        
        # Write the English version
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        count += 1
    
    print(f"  Total brand pages processed: {count}")
    return count

# ============================================================
# PROCESS OTHER PAGES
# ============================================================
def process_other_pages():
    """Process index, contacto, faq, quienes-somos, politica-privacidad, inspeccion-mecanica, servicios-domicilio, 404"""
    print("\n=== Step 6: Processing other pages ===")
    count = 0
    
    other_pages = {
        'index.html': 'index.html',
        'contacto.html': 'contacto.html',
        'faq.html': 'faq.html',
        'quienes-somos.html': 'about-us.html',
        'politica-privacidad.html': 'privacy-policy.html',
        'inspeccion-mecanica.html': 'mechanical-inspection.html',
        'servicios-domicilio.html': 'services-at-home.html',
        '404.html': '404.html',
    }
    
    for es_filename, en_filename in other_pages.items():
        es_file = os.path.join(BASE, es_filename)
        en_file = os.path.join(EN_BASE, en_filename)
        
        if not os.path.exists(es_file):
            print(f"  WARNING: Missing {es_file}")
            continue
        
        with open(es_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Apply global replacements
        html = apply_replacements(html)
        
        # Fix JSON-LD
        html = fix_jsonld(html, 'other')
        
        # Calculate en_path for hreflang
        en_path = f'/en/{en_filename}'
        
        # Fix canonical and hreflang
        html = fix_canonical_hreflang(html, en_path)
        
        # Fix nav URLs
        html = fix_nav_urls(html)
        
        # Add language switcher
        html = add_lang_switcher(html, en_path)
        
        # Write the English version
        os.makedirs(os.path.dirname(en_file), exist_ok=True)
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        count += 1
        print(f"  Processed: {es_filename} -> {en_filename}")
    
    print(f"  Total other pages processed: {count}")
    return count

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("MECANICO247.COM ENGLISH TRANSLATION SCRIPT")
    print("=" * 60)
    
    # Step 1: Clean up
    cleanup_en()
    
    # Step 2: Process comuna pages
    comuna_count = process_comunas()
    
    # Step 3: Process service pages
    service_count = process_services()
    
    # Step 4: Process vehicle pages
    vehicle_count = process_vehicles()
    
    # Step 5: Process brand pages
    brand_count = process_brands()
    
    # Step 6: Process other pages
    other_count = process_other_pages()
    
    total = comuna_count + service_count + vehicle_count + brand_count + other_count
    
    print("\n" + "=" * 60)
    print(f"TRANSLATION COMPLETE!")
    print(f"  Comuna pages: {comuna_count}")
    print(f"  Service pages: {service_count}")
    print(f"  Vehicle pages: {vehicle_count}")
    print(f"  Brand pages: {brand_count}")
    print(f"  Other pages: {other_count}")
    print(f"  TOTAL: {total}")
    print("=" * 60)
