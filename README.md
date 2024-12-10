1. utilizar codigo python para obtener datos de la API sin duplicados

2. exportar datos de la BD con la sentencia select NOMBRE, IDREGISTRO, IDENTIFICACION from listascontroldetalle where listascontrol_id = 50;

3. comparar los dos archivos

4. RETIRAR (R) teniendo como referencia el archivo exportado de la BD
	NOMBRE | IDREGISTRO | IDENTIFICACION | BD EN API | API
	=SI(CONTAR.SI(E:E; C610)>0; "Sí"; "No")
	se eliminan los filtrados con No

5. ACTUALIZAR (A) teniendo como referencia el archivo exportado de la API
	Descripción/Resumen | Entidad | Fecha de Vinculación | Departamento	Municipio | Nombre Completo (Apellidos-Nombres) /Razón Social | Tipo de Documento | No. De documento | A | IDREGISTRO | IDENTIFICACION
	=BUSCARX(H2; K:K; J:J; ""; 0; 1)
	se actualizan los asignados ya que esto indica que las identificaciones de los registros en la BD ya existen en la API, por lo tanto deben tener la información más reciente
	
6. INGRESAR (I)
