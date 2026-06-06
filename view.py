import streamlit as st
import pandas as pd

def inicializar_vista_web(controlador):
    sectores_dict = {
        1: "🥛 Bebidas y Lácteos Básicos", 2: "🧼 Limpieza e Higiene Hogar", 3: "🥔 Verdulería Pesada",
        4: "🥬 Verdulería Liviana y Hojas", 5: "🥫 Almacén, Pastas y Latas", 6: "☕ Desayuno y Merienda",
        7: "🥚 Panadería y Huevos", 8: "🧻 Servilletas y Papeles", 9: "👶 Sector Bebés",
        10: "🧴 Perfumería y Cuidado Personal", 11: "🥩 Carnicería y Fiambrería",
        12: "🧀 Refrigerados y Congelados", 99: "📦 Ítems Sin Asignar"
    }

    colores_sectores = {
        1: {"bg": "#F0F7FF", "text": "#1E3A8A", "border": "#3B82F6"}, 2: {"bg": "#F0FDF4", "text": "#14532D", "border": "#22C55E"},
        3: {"bg": "#FEFCE8", "text": "#713F12", "border": "#EAB308"}, 4: {"bg": "#F0FDF4", "text": "#166534", "border": "#4ADE80"},
        5: {"bg": "#FAF5FF", "text": "#581C87", "border": "#A855F7"}, 6: {"bg": "#FFF7ED", "text": "#7C2D12", "border": "#FB923C"},
        7: {"bg": "#FAFAF9", "text": "#44403C", "border": "#A8A29E"}, 8: {"bg": "#F8FAFC", "text": "#334155", "border": "#94A3B8"},
        9: {"bg": "#F0F9FF", "text": "#0C4A6E", "border": "#38BDF8"}, 10: {"bg": "#FDF2F8", "text": "#701A75", "border": "#F472B6"},
        11: {"bg": "#FEF2F2", "text": "#7F1D1D", "border": "#F87171"}, 12: {"bg": "#E6F4F1", "text": "#044E44", "border": "#0D9488"},
        99: {"bg": "#FAFAFA", "text": "#262626", "border": "#D4D4D4"}
    }

    # Inyección de Estilos de Nivel Avanzado (UI/UX Premium)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Variables de diseño y reinicio */
    .stApp { background-color: #F8FAFC; font-family: 'Plus Jakarta Sans', sans-serif !important; }
    h1, h2, h3, h4 { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #0F172A; }
    
    /* Encabezado Principal de Alta Gama */
    .header-container { 
        text-align: center; 
        padding: 35px 20px; 
        background: linear-gradient(135deg, #047857 0%, #065F46 100%); 
        border-radius: 24px; 
        box-shadow: 0 20px 40px -15px rgba(4, 120, 87, 0.25); 
        margin-bottom: 35px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Pestañas de Navegación Rediseñadas */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; justify-content: center; background-color: #F1F5F9; padding: 8px; border-radius: 16px; border: 1px solid #E2E8F0; }
    .stTabs [data-baseweb="tab"] { height: 44px; background-color: transparent; border-radius: 12px; font-weight: 700; font-size: 0.95rem; color: #64748B; border: none !important; padding: 0px 24px; transition: all 0.2s ease; }
    .stTabs [aria-selected="true"] { background-color: #FFFFFF !important; color: #047857 !important; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -4px rgba(0,0,0,0.05); }
    
    /* Tarjetas de Contenedores Tipo SaaS */
    .card-premium { 
        background: #FFFFFF; 
        padding: 26px; 
        border-radius: 20px; 
        border: 1px solid #E2E8F0; 
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.02), 0 10px 15px -3px rgba(15, 23, 42, 0.03); 
        margin-bottom: 25px; 
    }
    
    /* Indicadores Rápidos (KPIs) */
    .metric-badge {
        background: #FFFFFF; padding: 12px 16px; border-radius: 14px; text-align: center; border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
    }
    
    /* Botonera Global Unificada */
    .stButton button { border-radius: 12px !important; font-weight: 700 !important; font-size: 0.95rem !important; padding: 10px 20px !important; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; }
    .stButton button[type="primary"] { background: linear-gradient(135deg, #059669 0%, #047857 100%) !important; border: none !important; color: white !important; box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3); }
    .stButton button[type="primary"]:hover { transform: translateY(-1px) scale(1.01); box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4); }
    
    /* Botones de acción secundaria (Quitar de la lista) */
    div[data-testid="stColumn"] .stButton button { background-color: #FEF2F2 !important; color: #EF4444 !important; border: 1px solid #FEE2E2 !important; font-size: 0.85rem !important; padding: 6px 12px !important; margin-top: 10px; }
    div[data-testid="stColumn"] .stButton button:hover { background-color: #EF4444 !important; color: white !important; border-color: #EF4444 !important; transform: translateY(-0.5px); }
    
    /* Tarjetas Interactivas de los Productos Activos */
    .item-compra-card { 
        padding: 16px 18px; 
        border-radius: 16px; 
        margin-bottom: 10px; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01), 0 2px 4px -1px rgba(0, 0, 0, 0.01); 
        transition: transform 0.2s ease;
    }
    .item-compra-card:hover { transform: translateX(2px); }
    </style>
    """, unsafe_allow_html=True)

    # 1. PANTALLA DE CONTROL DE ACCESO (LOGIN)
    if "usuario" not in st.session_state:
        col_login_centrar, col_login_body, col_login_der = st.columns([0.8, 2, 0.8])
        
        with col_login_body:
            st.markdown("<div class='header-container'><h1 style='color:white; margin:0; font-size:2.6rem; font-weight:800; letter-spacing:1px;'>🛒 CARREFULL</h1><p style='color:#A7F3D0;margin:6px 0 0 0; font-weight:600; font-size:1.05rem; opacity:0.95;'>Gestión Logística del Hogar</p></div>", unsafe_allow_html=True)
            
            tab_log, tab_reg = st.tabs(["🔑 Ingresar al Panel", "👤 Registrar Nuevo Miembro"])
            
            with tab_log:
                st.markdown("<div class='card-premium'>", unsafe_allow_html=True)
                st.markdown("<h3 style='margin-top:0; font-size:1.35rem; font-weight:700;'>Identificación</h3>", unsafe_allow_html=True)
                email = st.text_input("Correo Registrado:", key="login_email", placeholder="nombre@correo.com")
                password = st.text_input("Contraseña Privada:", type="password", key="login_pass", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("ACCEDER AL ENTORNO", use_container_width=True, type="primary"):
                    user_data = controlador.autenticar_usuario(email, password)
                    if user_data:
                        st.session_state.usuario = user_data
                        st.rerun()
                    else:
                        st.error("Credenciales inválidas o usuario no autorizado.")
                st.markdown("</div>", unsafe_allow_html=True)
                        
            with tab_reg:
                st.markdown("<div class='card-premium'>", unsafe_allow_html=True)
                st.markdown("<h3 style='margin-top:0; font-size:1.35rem; font-weight:700;'>Alta Familiar Directa</h3>", unsafe_allow_html=True)
                reg_nombre = st.text_input("Nombre de Pila:", placeholder="Ej: Paula, Francisco")
                reg_email = st.text_input("Email de Acceso:", placeholder="familiar@correo.com")
                reg_pass = st.text_input("Establecer Contraseña:", type="password", placeholder="Mínimo 6 caracteres")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("CONFIRMAR ALTA DE CUENTA", use_container_width=True, type="primary"):
                    if reg_nombre and reg_email and reg_pass:
                        if controlador.registrar_nuevo_usuario(reg_email, reg_pass, reg_nombre):
                            st.success("¡Cuenta configurada con éxito! Ya podés loguearte.")
                        else:
                            st.error("Este identificador ya se encuentra registrado.")
                    else:
                        st.error("Por favor completá todas las casillas requeridas.")
                st.markdown("</div>", unsafe_allow_html=True)
        return

    # 2. ENTORNO DE COMPRAS LOGUEADO
    u_id = st.session_state.usuario["id"]
    u_nombre = st.session_state.usuario["nombre"]

    # Header Principal de la Plataforma Activa
    st.markdown(f"""
    <div class="header-container">
        <h1 style='color: #FFFFFF; font-weight: 800; font-size: 2.5rem; margin: 0; letter-spacing: 0.5px;'>🛒 CARREFULL</h1>
        <p style='color: #A7F3D0; font-size: 1.05rem; font-weight: 600; margin: 8px 0 0 0; opacity:0.95;'>Sistema de Abastecimiento de {u_nombre}</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Lateral Profesional
    st.sidebar.markdown(f"### 👤 Perfil: **{u_nombre}**")
    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 Cerrar Entorno Seguro", use_container_width=True):
        del st.session_state.usuario
        st.rerun()

    tab_lista, tab_recetas, tab_maestro = st.tabs(["⚡ Panel de Abastecimiento", "🍳 Automatización de Menús", "⚙️ Catálogo Maestro"])

    with tab_lista:
        col_ingreso, col_hoja_ruta = st.columns([1, 1.1], gap="large")
        
        with col_ingreso:
            # Bloque Superior: Inyección por Recetas
            st.markdown('<div class="card-premium">', unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top:0; font-size:1.3rem; font-weight:700;'>✨ Cargar Plato Planificado</h3>", unsafe_allow_html=True)
            recetas = controlador.obtener_recetas_catalogo(u_id)
            lista_recetas = [f"{r[0]}: {r[1].upper()}" for r in recetas]
            
            receta_seleccionada = st.selectbox("Elegí una receta guardada de tu menú:", [""] + lista_recetas, key="sb_receta_fast")
            
            if receta_seleccionada:
                receta_id = int(receta_seleccionada.split(":")[0])
                nombre_plato = receta_seleccionada.split(":")[1].strip()
                ingredientes = controlador.obtener_ingredientes_receta(receta_id)
                
                if ingredientes:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander(f"📋 Auditoría de Faltantes: {nombre_plato}", expanded=True):
                        dict_checks = {}
                        for idx, ing in enumerate(ingredientes):
                            prod_name, cant, unidad = ing
                            txt_display = f"Falta {prod_name.capitalize()} ({cant} {unidad})"
                            dict_checks[ing] = st.checkbox(txt_display, value=True, key=f"chk_ing_{receta_id}_{idx}")
                        
                        nota_batch = st.text_input("Anotación para el lote:", placeholder="Ej: Compras para el fin de semana", key="nota_rec")
                        if st.button("🚀 INYECTAR FALTANTES SELECCIONADOS", use_container_width=True, type="primary"):
                            for ing, faltante in dict_checks.items():
                                if faltante:
                                    controlador.agregar_a_lista(u_id, ing[0], ing[1], ing[2], nota_batch if nota_batch else f"Receta: {nombre_plato}")
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # Bloque Inferior: Adición Manual Rápida
            st.markdown('<div class="card-premium">', unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top:0; font-size:1.3rem; font-weight:700;'>➕ Agregar Artículo Suelto</h3>", unsafe_allow_html=True)
            productos_maestro = controlador.obtener_lista_productos_maestro(u_id)
            lista_nombres_maestro = [p[0].capitalize() for p in productos_maestro]
            
            prod_manual = st.selectbox("Buscar en el maestro indexado:", [""] + lista_nombres_maestro)
            
            col_c, col_u = st.columns(2)
            with col_c: 
                cant_m = st.number_input("Establecer Volumen:", min_value=0.1, value=1.0, step=0.5)
            with col_u: 
                uni_m = st.selectbox("Unidad Métrica:", ["unidades", "gramos", "kilos"])
                
            obs_m = st.text_input("Comentario específico:", placeholder="Ej: Marca premium, bajo en sodio")
            
            if st.button("Sumar de Inmediato a la Lista", use_container_width=True, type="primary"):
                if prod_manual:
                    controlador.agregar_a_lista(u_id, prod_manual.lower(), cant_m, uni_m, obs_m)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_hoja_ruta:
            registros = controlador.obtener_compras_activas(u_id)
            
            # Encabezado con métrica dinámica de impacto
            st.markdown("<h2 style='margin-top:0; font-size:1.5rem; font-weight:700;'>📋 Hoja de Ruta Inteligente</h2>", unsafe_allow_html=True)
            
            if not registros:
                st.info("La lista se encuentra vacía. Agregá componentes a la izquierda para calcular tu ruta óptima.")
            else:
                # Indicadores de estado elegantes en la parte superior derecha
                cant_items = len(registros)
                sectores_unicos = len(set([r[2] for r in registros]))
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.markdown(f"<div class='metric-badge'><small style='color:#64748B;font-weight:600;'>PRODUCTOS TOTALES</small><br><b style='font-size:1.4rem;color:#047857;'>{cant_items}</b></div>", unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"<div class='metric-badge'><small style='color:#64748B;font-weight:600;'>SECTORES DE GÓNDOLA</small><br><b style='font-size:1.4rem;color:#0F172A;'>{sectores_unicos}</b></div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Despliegue secuencial de la lista optimizada
                for reg in registros:
                    compra_id, fecha, sector_id, prod_name, cant, unidad, obs = reg
                    c = colores_sectores.get(sector_id, {"bg": "#FAFAFA", "text": "#262626", "border": "#D4D4D4"})
                    
                    col_card, col_btn = st.columns([4.8, 1.2])
                    
                    with col_card:
                        card_html = f"""
                        <div class="item-compra-card" style="background-color: {c['bg']}; border-left: 6px solid {c['border']}; color: {c['text']};">
                            <div style="font-size:0.75rem; font-weight:800; text-transform:uppercase; color:{c['border']}; letter-spacing:0.3px; margin-bottom: 3px;">{sectores_dict.get(sector_id, 'Sin sector')}</div>
                            <div style="font-size:1.1rem; font-weight:700;">{prod_name.capitalize()} <span style="font-weight:500; font-size:0.95rem; opacity:0.8;">({cant} {unidad})</span></div>
                            {f'<div style="font-size:0.8rem; margin-top:6px; opacity:0.85; border-top: 1px dashed rgba(0,0,0,0.05); padding-top: 4px;">📝 {obs}</div>' if obs else ''}
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                    with col_btn:
                        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                        if st.button("Quitar", key=f"del_{compra_id}", use_container_width=True):
                            controlador.borrar_compra(compra_id, u_id)
                            st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.divider()
                
                exito, resultado = controlador.procesar_cierre_y_exportacion(u_id, sectores_dict)
                if exito:
                    st.download_button(
                        label="🏁 CONCLUIR COMPRA Y EXPORTAR (CSV)",
                        data=resultado,
                        file_name=f"hoja_ruta_{u_nombre.lower()}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        type="primary"
                    )

    with tab_recetas:
        st.markdown('<div class="card-premium">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; font-size:1.3rem; font-weight:700;'>🧑‍🍳 Diseñar Nueva Receta Familiar</h3>", unsafe_allow_html=True)
        nombre_receta = st.text_input("Nombre de la Receta:", placeholder="Ej: Canelones de verdura, Pollo al horno con papas").strip()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card-premium">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; font-size:1.1rem; font-weight:700;'>🥦 Añadir Componentes Obligatorios</h4>", unsafe_allow_html=True)
        
        col_ing_n, col_ing_c, col_ing_u = st.columns([2, 1, 1])
        with col_ing_n:
            ing_nombre = st.text_input("Alimento / Ingrediente:", placeholder="Ej: Puré de tomate")
        with col_ing_c:
            ing_cant = st.number_input("Volumen Requerido:", min_value=0.1, value=1.0, step=0.5, key="rec_cant")
        with col_ing_u:
            ing_uni = st.selectbox("Unidad:", ["unidades", "gramos", "kilos"], key="rec_uni")
        
        if st.button("➕ Vincular al Borrador Temporal", use_container_width=True):
            if ing_nombre:
                if "borrador" not in st.session_state: st.session_state.borrador = []
                st.session_state.borrador.append((ing_nombre.lower(), ing_cant, ing_uni))
                st.toast(f"✔ '{ing_nombre.capitalize()}' añadido al esquema preliminar.")
        st.markdown('</div>', unsafe_allow_html=True)

        if "borrador" in st.session_state and st.session_state.borrador:
            st.markdown('<div class="card-premium">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top:0;'>Esquema de Compras del Plato</h4>", unsafe_allow_html=True)
            df_d = pd.DataFrame(st.session_state.borrador, columns=["Ingrediente", "Cantidad", "Unidad"])
            st.dataframe(df_d, use_container_width=True, hide_index=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Descartar Borrador", use_container_width=True):
                    st.session_state.borrador = []
                    st.rerun()
            with col_b2:
                if st.button("💾 COMPILAR E INDEXAR RECETA", use_container_width=True, type="primary"):
                    if nombre_receta:
                        if controlador.crear_receta_completa(u_id, nombre_receta, st.session_state.borrador):
                            st.success(f"¡Receta '{nombre_receta.capitalize()}' consolidada e indexada con éxito!")
                            st.session_state.borrador = []
                            st.rerun()
                        else: st.error("Ya existe una receta con esa denominación exacta.")
                    else: st.error("Falta especificar el nombre principal de la receta arriba.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_maestro:
        st.markdown('<div class="card-premium">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; font-size:1.3rem; font-weight:700;'>⚙️ Indexación y Mapeo de Góndolas</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#475569;font-size:0.92rem;margin-bottom:20px;'>Para garantizar el ordenamiento lógico e inteligente de tu lista, debés emparejar los artículos que compras usualmente con el pasillo correspondiente en el supermercado físico.</p>", unsafe_allow_html=True)
        
        m_nombre = st.text_input("Nombre de Referencia Técnico:", placeholder="Ej: Tapas de empanada, Papel higiénico, Pechuga")
        opciones_s = [f"{k}: {v}" for k, v in sectores_dict.items() if k != 99]
        m_sector_sel = st.selectbox("Asignación de Pasillo / Sector:", opciones_s)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Registrar en mi Base de Datos Maestra", use_container_width=True, type="primary"):
            if m_nombre:
                s_id = int(m_sector_sel.split(":")[0])
                if controlador.crear_producto_maestro(u_id, m_nombre, s_id):
                    st.success(f"¡El artículo '{m_nombre.capitalize()}' fue mapeado y guardado!")
                    st.rerun()
                else: st.warning("Este artículo ya se encuentra registrado en tu catálogo.")
            else:
                st.error("Por favor, indicá el nombre de referencia técnico.")
        st.markdown('</div>', unsafe_allow_html=True)