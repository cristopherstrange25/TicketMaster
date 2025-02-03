#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void limpiarPantalla() {
    // Imprimir varias l?neas en blanco
    printf("\n\n\n\n");
}

int esBisiesto(int anio) {
    if ((anio % 4 == 0 && anio % 100 != 0) || (anio % 400 == 0)) {
        return 1; // Es bisiesto
    }
    return 0; // No es bisiesto
}

int esDiaFestivo(int dia, int mes, int anio) {
    return (dia == 1 && mes == 1) ||  // A?o Nuevo (1 de enero)
           (dia == 3 && mes == 2) ||  // D?a de la Constituci?n (primer lunes de febrero)
           (dia == 17 && mes == 3) || // Natalicio de Benito Ju?rez (tercer lunes de marzo)
           (dia == 17 && mes == 4) || // Jueves Santo (Semana Santa)
           (dia == 18 && mes == 4) || // Viernes Santo (Semana Santa)
           (dia == 1 && mes == 5) ||  // D?a del Trabajo (1 de mayo)
           (dia == 16 && mes == 9) || // D?a de la Independencia (16 de septiembre)
           (dia == 17 && mes == 11) || // D?a de la Revoluci?n (tercer lunes de noviembre)
           (dia == 25 && mes == 12);  // Navidad (25 de diciembre)
}

void elegirTeatro() {
    int teatro, obra, horario, cantidadBoletos, seccion;
    float precio, total;
    char metodo[50], numeroTarjeta[20], nombreTitular[50];
    char lugar[100], horarioSeleccionado[30], obraSeleccionada[30];
    int dia, mes, anio;
    char continuar = 'n';
	do {
    // Opciones de teatro
printf("\nElige un teatro:\n");
    printf("1. Teatro Col?n, Buenos Aires... Capacidad: 2500 personas\n");
    printf("2. Teatro de la Scala, Mil?n... Capacidad: 2800 personas\n");
    printf("3. Teatro Metropolit?n, Ciudad de M?xico... Capacidad: 8000 personas\n");
    printf("Selecciona un teatro: ");
    scanf("%d", &teatro);
    
    switch (teatro) {
        case 1:
            printf("Has seleccionado el Teatro Col?n, Buenos Aires.\n");
            printf("Capacidad: 2500 personas.\n");
            break;
        case 2:
            printf("Has seleccionado el Teatro de la Scala, Mil?n.\n");
            printf("Capacidad: 2800 personas.\n");
            break;
        case 3:
            printf("Has seleccionado el Teatro Metropolit?n, Ciudad de M?xico.\n");
            printf("Capacidad: 8000 personas.\n");
            break;
        default:
            printf("Opci?n inv?lida.\n");
            return;  // Termina el programa si la opci?n es inv?lida.
    }
    
    // Solicitar fecha
    printf("\nIngresa la fecha (d?a, mes y a?o) de la funci?n:\n");
    printf("D?a: ");
    scanf("%d", &dia);
    printf("Mes: ");
    scanf("%d", &mes);
    printf("A?o: ");
    scanf("%d", &anio);
    
    // Verificar si el mes es v?lido (1 a 12)
    if (mes < 1 || mes > 12) {
    	printf("\n ....Fecha no valida....");
    	while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
    }

    // D?as por mes (enero, marzo, mayo, julio, agosto, octubre, diciembre tienen 31 d?as)
    int diasPorMes[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    // Si es febrero y el a?o es bisiesto, ajustamos el n?mero de d?as a 29
    if (mes == 2 && esBisiesto(anio)) {
        diasPorMes[2] = 29;
    }

    // Verificar si el d?a es v?lido para el mes
    if (dia < 1 || dia > diasPorMes[mes]) {
        printf("\n ....Fecha no valida....");
        while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
    }
    
    if(anio<2025 or anio>9999){
    	printf("\n ....Fecha no valida....");
    	while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
	} 

    // Verificar si es d?a festivo
    if (esDiaFestivo(dia, mes, anio)) {
    char cont = 'n';
    printf("\n\nNo es posible comprar boletos en d?as festivos.\n");
    printf("Estos son los d?as festivos de 2025 en M?xico:\n");
    printf("  - 1 de enero: A?o Nuevo\n");
    printf("  - 3 de febrero: D?a de la Constituci?n (lunes)\n");
    printf("  - 17 de marzo: Natalicio de Benito Ju?rez (lunes)\n");
    printf("  - 17 de abril: Jueves Santo\n");
    printf("  - 18 de abril: Viernes Santo\n");
    printf("  - 1 de mayo: D?a del Trabajo\n");
    printf("  - 16 de septiembre: D?a de la Independencia\n");
    printf("  - 17 de noviembre: D?a de la Revoluci?n (lunes)\n");
    printf("  - 25 de diciembre: Navidad\n\n");
    printf("Regresando al men? principal...\n\n");
    
    while (getchar() != '\n'); // Espera que el usuario presione Enter
    getchar();
    return;
}


    // Determinar las obras seg?n el teatro
    printf("\nSelecciona una obra para el teatro elegido:\n");
    printf("1. El rey Le?n A\n");
    printf("2. Frankenstein B\n");
    printf("3. Romeo y Julieta C\n");
    printf("Selecciona una obra: ");
    scanf("%d", &obra);
    // Determinar la obra seleccionada
    switch (obra) {
        case 1: strcpy(obraSeleccionada, "El rey Le?n"); break;
        case 2: strcpy(obraSeleccionada, "Frankenstein"); break;
        case 3: strcpy(obraSeleccionada, "Romeo y Julieta"); break;
        default: printf("Opci?n inv?lida.\n"); return;
    }

    // Opciones de horarios seg?n la obra
    printf("\nSelecciona un horario para la obra seleccionada:\n");
    printf("1. 3:00 PM - 4:00 PM\n");
    printf("2. 4:00 PM - 5:00 PM\n");
    printf("3. 5:00 PM - 6:00 PM\n");
    printf("Selecciona un horario: ");
    scanf("%d", &horario);
    // Determinar el horario seleccionado
    switch (horario) {
        case 1: strcpy(horarioSeleccionado, "3:00 PM - 4:00 PM"); break;
        case 2: strcpy(horarioSeleccionado, "4:00 PM - 5:00 PM"); break;
        case 3: strcpy(horarioSeleccionado, "5:00 PM - 6:00 PM"); break;
        default: printf("Opci?n inv?lida.\n"); return;
    }

    // Secci?n y precio
    printf("\nElige la secci?n:\n");
    printf("1. Luneta - $500\n");
    printf("2. Palco - $800\n");
    printf("3. Galer?a - $300\n");
    printf("Selecciona la secci?n: ");
    scanf("%d", &seccion);

    switch (seccion) {
        case 1: precio = 500; break;
        case 2: precio = 800; break;
        case 3: precio = 300; break;
        default: printf("Opci?n inv?lida.\n"); return;
    }

    // Capacidad del lugar (m?xima seg?n el teatro)
    int capacidad;
    if (teatro == 1) {
        capacidad = 2500; // Teatro Col?n
        strcpy(lugar, "Teatro Col?n, Buenos Aires");
    }
    else if (teatro == 2) {
        capacidad = 2800; // Teatro de la Scala
        strcpy(lugar, "Teatro de la Scala, Mil?n");
    }
    else if (teatro == 3) {
        capacidad = 8000; // Teatro Metropolit?n
        strcpy(lugar, "Teatro Metropolit?n, Ciudad de M?xico");
    } else {
        capacidad = 0;
    }

    printf("\nLa capacidad m?xima del lugar es %d personas.\n", capacidad);

    // Cantidad de boletos
    printf("\n?Cu?ntos boletos deseas comprar? (m?ximo 10): ");
    scanf("%d", &cantidadBoletos);
    if (cantidadBoletos > 10) {
        printf("No puedes comprar m?s de 10 boletos.\n");
        return;
    }
    if (cantidadBoletos > capacidad) {
        printf("No hay suficientes boletos disponibles. Solo quedan %d boletos.\n", capacidad);
        return;
    }

    

    

    // Mostrar total
    total = precio * cantidadBoletos;
    printf("\nCantidad de boletos: %d\n", cantidadBoletos);
    printf("Precio por boleto: $%.2f\n", precio);
    printf("Total a pagar: $%.2f\n", total);
    printf("\nTipo de vestimenta: Formal (Traje o vestido elegante).\n");

    // Ingreso de datos de pago
        int metodoPago;
    
    printf("\nElige el m?todo de pago:\n");
    printf("1. Tarjeta de d?bito\n");
    printf("2. Tarjeta de cr?dito\n");
    printf("3. PayPal\n");
    printf("Selecciona un m?todo de pago: ");
    scanf("%d", &metodoPago);

    switch (metodoPago) {
        case 1:
            strcpy(metodo, "Tarjeta de d?bito");
            printf("Ingresa el n?mero de tarjeta (solo n?meros): ");
            scanf("%s", numeroTarjeta);
            printf("Ingresa el nombre del titular: ");
            scanf(" %[^\n]", nombreTitular); // Leer nombres con espacios
            break;
        case 2:
            strcpy(metodo, "Tarjeta de cr?dito");
            printf("Ingresa el n?mero de tarjeta (solo n?meros): ");
            scanf("%s", numeroTarjeta);
            printf("Ingresa el nombre del titular: ");
            scanf(" %[^\n]", nombreTitular); // Leer nombres con espacios
            break;
        case 3:
            strcpy(metodo, "PayPal");
            printf("Ingresa el correo electr?nico asociado a PayPal: ");
            scanf("%s", numeroTarjeta);
            printf("Ingresa el nombre del titular: ");
            scanf(" %[^\n]", nombreTitular); // Leer nombres con espacios
            break;
        default:
            printf("Opci?n inv?lida.\n");
            return;
    }

    // Resumen final
    printf("\n--- Resumen de la compra ---\n");
    printf("Estudiante: Cristopher Celestino Martinez\n");
    printf("Teatro: %s\n", lugar);
    printf("Obra: %s\n", obraSeleccionada);
    printf("Fecha: %02d/%02d/%d\n", dia, mes, anio);
    printf("Horario: %s\n", horarioSeleccionado);
    printf("Secci?n: %s\n", (seccion == 1) ? "Luneta" : (seccion == 2) ? "Palco" : "Galer?a");
    printf("Cantidad de boletos: %d\n", cantidadBoletos);
    printf("Total a pagar: $%.2f\n", total);
    printf("M?todo de pago: %s\n", metodo);
    if (strcmp(metodo, "PayPal") == 0) {
        printf("Correo asociado: %s\n", numeroTarjeta);
        printf("Titular: %s\n", nombreTitular);
    } else {
        printf("N?mero de tarjeta: %s\n", numeroTarjeta);
        printf("Titular: %s\n", nombreTitular);
    }
    printf("Tipo de vestimenta: Formal (Traje o vestido elegante).\n");
    
    printf("\n?Desea realizar otra compra? (s/n): ");
        scanf(" %c", &continuar);
        limpiarPantalla();
    } while (continuar == 's');
}

// Funci?n que encapsula todo el proceso de elegir cine y realizar la compra
void elegirCine() {
	char cine[30];
    char horario[20];
    char pelicula[60];
    char metodoPago[50];
    char nombrePago[50];
    char numeroTarjeta[20];
    float precio;
    int cantidadBoletos;
    char servicio[20];
    char asientos[100];
    int opcion, opcionPelicula, opcionHorario, opcionServicio;
    char continuar = 'n';
    int dia, mes, anio;
    char metodo[40]; 
	char nombreTitular[40];
    do {
        // Selecci?n de cine
        printf("\nSeleccione el cine:\n");
        printf("1. Cinemark\n");
        printf("2. Cin?polis\n");
        printf("3. Cinemex\n");
        printf("4. AMC\n");
        printf("Opci?n: ");
        scanf("%d", &opcion);

        switch (opcion) {
            case 1: strcpy(cine, "Cinemark"); break;
            case 2: strcpy(cine, "Cin?polis"); break;
            case 3: strcpy(cine, "Cinemex"); break;
            case 4: strcpy(cine, "AMC"); break;
            default: printf("Opci?n inv?lida.\n"); return;
        }
        
        // Solicitar fecha
    	printf("\nIngresa la fecha (d?a, mes y a?o) de la funci?n:\n");
 	    printf("D?a: ");
    	scanf("%d", &dia);
    	printf("Mes: ");
    	scanf("%d", &mes);
    	printf("A?o: ");
    	scanf("%d", &anio);
    	
    	 // Verificar si el mes es v?lido (1 a 12)
    if (mes < 1 || mes > 12) {
    	printf("\n ....Fecha no valida....");
    	while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
    }

    // D?as por mes (enero, marzo, mayo, julio, agosto, octubre, diciembre tienen 31 d?as)
    int diasPorMes[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    // Si es febrero y el a?o es bisiesto, ajustamos el n?mero de d?as a 29
    if (mes == 2 && esBisiesto(anio)) {
        diasPorMes[2] = 29;
    }

    // Verificar si el d?a es v?lido para el mes
    if (dia < 1 || dia > diasPorMes[mes]) {
        printf("\n ....Fecha no valida....");
        while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
    }
    if(anio<2025 or anio>9999){
    	printf("\n ....Fecha no valida....");
    	while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
	} 

    	// Verificar si es d?a festivo
    	if (esDiaFestivo(dia, mes, anio)) {
    char cont = 'n';
    printf("\n\nNo es posible comprar boletos en d?as festivos.\n");
    printf("Estos son los d?as festivos de 2025 en M?xico:\n");
    printf("  - 1 de enero: A?o Nuevo\n");
    printf("  - 3 de febrero: D?a de la Constituci?n (lunes)\n");
    printf("  - 17 de marzo: Natalicio de Benito Ju?rez (lunes)\n");
    printf("  - 17 de abril: Jueves Santo\n");
    printf("  - 18 de abril: Viernes Santo\n");
    printf("  - 1 de mayo: D?a del Trabajo\n");
    printf("  - 16 de septiembre: D?a de la Independencia\n");
    printf("  - 17 de noviembre: D?a de la Revoluci?n (lunes)\n");
    printf("  - 25 de diciembre: Navidad\n\n");
    printf("Regresando al men? principal...\n\n");
    
    while (getchar() != '\n'); // Espera que el usuario presione Enter
    getchar();
    return;
}

       

        printf("\nSeleccione la pel?cula:\n");
    printf("1. Avatar: El Camino del Agua (PG-13)\n");
    printf("2. Spider-Man: Cruzando el Multiverso (PG)\n");
    printf("3. John Wick 4 (R)\n");
    printf("4. Mario Bros: La Pel?cula (PG)\n");
    printf("Opci?n: ");
    scanf("%d", &opcionPelicula);

    switch (opcionPelicula) {
        case 1:
            strcpy(pelicula, "Avatar: El Camino del Agua");
            printf("\nClasificaci?n: PG-13\n");
            printf("Restricciones: No se permite el ingreso con mascotas, armas ni alimentos.\n");
            break;
        case 2:
            strcpy(pelicula, "Spider-Man: Cruzando el Multiverso");
            printf("\nClasificaci?n: PG\n");
            printf("Restricciones: No se permite el ingreso con mascotas ni armas. Se permite alimentos ligeros.\n");
            break;
        case 3:
            strcpy(pelicula, "John Wick 4");
            printf("\nClasificaci?n: R\n");
            printf("Restricciones: No se permite el ingreso con mascotas ni alimentos. Las armas son permitidas solo con licencia.\n");
            break;
        case 4:
            strcpy(pelicula, "Mario Bros: La Pel?cula");
            printf("\nClasificaci?n: PG\n");
            printf("Restricciones: No se permite el ingreso con armas ni mascotas. Se permite ingresar con alimentos.\n");
            break;
        default:
            printf("Opci?n inv?lida.\n"); return;
    }

    // Mostrar la pel?cula seleccionada
    printf("\nPel?cula seleccionada: %s\n", pelicula);

        // Selecci?n de horario
        printf("\nSeleccione el horario para '%s':\n", pelicula);
        printf("1. 12:00 - 14:00\n");
        printf("2. 15:00 - 17:00\n");
        printf("3. 18:00 - 20:00\n");
        printf("Opci?n: ");
        scanf("%d", &opcionHorario);

        switch (opcionHorario) {
            case 1: strcpy(horario, "12:00 - 14:00"); break;
            case 2: strcpy(horario, "15:00 - 17:00"); break;
            case 3: strcpy(horario, "18:00 - 20:00"); break;
            default: 
                printf("Opci?n inv?lida.\n"); return;
        }

        // Selecci?n de servicio
        printf("\nSeleccione el tipo de servicio:\n");
        printf("1. Tradicional ($100.00)\n");
        printf("2. PLUUS ($120.00)\n");
        printf("3. VIP ($150.00)\n");
        printf("4. Macro XE ($140.00)\n");
        printf("5. Cin?polis Junior ($110.00)\n");
        printf("6. 4DX ($200.00)\n");
        printf("7. IMAX ($180.00)\n");
        printf("8. VR ($160.00)\n");
        printf("9. Screen X ($170.00)\n");
        printf("Opci?n: ");
        scanf("%d", &opcionServicio);

        switch (opcionServicio) {
            case 1: strcpy(servicio, "Tradicional"); precio = 100.00; break;
            case 2: strcpy(servicio, "PLUUS"); precio = 120.00; break;
            case 3: strcpy(servicio, "VIP"); precio = 150.00; break;
            case 4: strcpy(servicio, "Macro XE"); precio = 140.00; break;
            case 5: strcpy(servicio, "Cin?polis Junior"); precio = 110.00; break;
            case 6: strcpy(servicio, "4DX"); precio = 200.00; break;
            case 7: strcpy(servicio, "IMAX"); precio = 180.00; break;
            case 8: strcpy(servicio, "VR"); precio = 160.00; break;
            case 9: strcpy(servicio, "Screen X"); precio = 170.00; break;
            default: 
                printf("Opci?n inv?lida.\n"); return;
        }

        // Ingreso de datos de pago
        int metodoPago;
    
    printf("\nElige el m?todo de pago:\n");
    printf("1. Tarjeta de d?bito\n");
    printf("2. Tarjeta de cr?dito\n");
    printf("3. PayPal\n");
    printf("Selecciona un m?todo de pago: ");
    scanf("%d", &metodoPago);

    switch (metodoPago) {
        case 1:
            strcpy(metodo, "Tarjeta de d?bito");
            printf("Ingresa el n?mero de tarjeta (solo n?meros): ");
            scanf("%s", numeroTarjeta);
            printf("Ingresa el nombre del titular: ");
            scanf(" %[^\n]", nombreTitular); // Leer nombres con espacios
            break;
        case 2:
            strcpy(metodo, "Tarjeta de cr?dito");
            printf("Ingresa el n?mero de tarjeta (solo n?meros): ");
            scanf("%s", numeroTarjeta);
            printf("Ingresa el nombre del titular: ");
            scanf(" %[^\n]", nombreTitular); // Leer nombres con espacios
            break;
        case 3:
            strcpy(metodo, "PayPal");
            printf("Ingresa el correo electr?nico asociado a PayPal: ");
            scanf("%s", numeroTarjeta);
            printf("Ingresa el nombre del titular: ");
            scanf(" %[^\n]", nombreTitular); // Leer nombres con espacios
            break;
        default:
            printf("Opci?n inv?lida.\n"); return;
    }

        // Selecci?n de cantidad de boletos y asientos
        printf("\nIngrese la cantidad de boletos a comprar (m?ximo 10): ");
        scanf("%d", &cantidadBoletos);

        if (cantidadBoletos > 10) {
            printf("La cantidad m?xima de boletos es 10. Ajustando a 10.\n");
            cantidadBoletos = 10;
        }

        printf("Ingrese los n?meros de asiento (separados por comas): ");
        scanf(" %[^\n]", asientos);

        // Restricciones y clasificaci?n
        printf("\n--- Restricciones ---\n");
        printf("Clasificaci?n de pel?culas: G, PG, PG-13, R, NC-17.\n");
        printf("No se permite el acceso con:\n");
        printf("- Mascotas\n");
        printf("- Armas\n");
        printf("- Alimentos externos\n");
        printf("---------------------\n");

        // Mostrar informaci?n final
        printf("\n--- Detalles de la Compra ---\n");
        printf("Cine: %s\n", cine);
        printf("Fecha: %02d/%02d/%d\n", dia, mes, anio);
        printf("Horario: %s\n", horario);
        printf("Pel?cula: %s\n", pelicula);
        printf("Servicio: %s\n", servicio);
        printf("M?todo de Pago: %s\n", metodo);
        printf("Nombre: %s\n", nombreTitular);
        printf("N?mero de Tarjeta: %s\n", numeroTarjeta);
        printf("Cantidad de Boletos: %d\n", cantidadBoletos);
        printf("Asientos: %s\n", asientos);
        printf("Precio Total: %.2f\n", precio * cantidadBoletos);

        printf("\n?Desea realizar otra compra? (s/n): ");
        scanf(" %c", &continuar);
        limpiarPantalla();
    	} while (continuar == 's');
}

void elegirMuseo() {
    // Estructura para los datos de la compra
    typedef struct {
        char museo[50];
        char horario[30];
        char metodoPago[20];
        char nombrePago[50];
        char numeroTarjeta[20];
        float precio;
        int cantidadBoletos;
        char restricciones[100];
    } CompraMuseo;

    CompraMuseo compra;
    int opcion;
    char continuar = 'n';
    int dia, mes, anio;
    
    do {
        // Selecci?n de museo
        printf("\nSeleccione el museo:\n");
        printf("1. Museo de Louvre, Par?s\n");
        printf("2. Museo Metropolitano de Nueva York\n");
        printf("3. Museo Vaticano\n");
        printf("4. Museo Nacional de Antropolog?a, Ciudad de M?xico\n");
        printf("5. Museu Nacional d'Art de Catalunya\n");
        printf("Opci?n: ");
        scanf("%d", &opcion);

        switch (opcion) {
            case 1: strcpy(compra.museo, "Museo de Louvre, Par?s"); break;
            case 2: strcpy(compra.museo, "Museo Metropolitano de Nueva York"); break;
            case 3: strcpy(compra.museo, "Museo Vaticano"); break;
            case 4: strcpy(compra.museo, "Museo Nacional de Antropolog?a, Ciudad de M?xico"); break;
            case 5: strcpy(compra.museo, "Museu Nacional d'Art de Catalunya"); break;
            printf("Opci?n inv?lida.\n"); return;
        }
		
		// Solicitar fecha
    	printf("\nIngresa la fecha (d?a, mes y a?o) de la funci?n:\n");
    	printf("D?a: ");
    	scanf("%d", &dia);
    	printf("Mes: ");
    	scanf("%d", &mes);
    	printf("A?o: ");
    	scanf("%d", &anio);

		 // Verificar si el mes es v?lido (1 a 12)
    if (mes < 1 || mes > 12) {
    	printf("\n ....Fecha no valida....");
    	while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
    }

    // D?as por mes (enero, marzo, mayo, julio, agosto, octubre, diciembre tienen 31 d?as)
    int diasPorMes[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    // Si es febrero y el a?o es bisiesto, ajustamos el n?mero de d?as a 29
    if (mes == 2 && esBisiesto(anio)) {
        diasPorMes[2] = 29;
    }

    // Verificar si el d?a es v?lido para el mes
    if (dia < 1 || dia > diasPorMes[mes]) {
        printf("\n ....Fecha no valida....");
        while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
    }
    if(anio<2025 or anio>9999){
    	printf("\n ....Fecha no valida....");
    	while (getchar() != '\n'); // Espera que el usuario presione Enter
    	getchar();
        return; // Mes inv?lido
	} 
		
    	// Verificar si es d?a festivo
    	if (esDiaFestivo(dia, mes, anio)) {
    char cont = 'n';
    printf("\n\nNo es posible comprar boletos en d?as festivos.\n");
    printf("Estos son los d?as festivos de 2025 en M?xico:\n");
    printf("  - 1 de enero: A?o Nuevo\n");
    printf("  - 3 de febrero: D?a de la Constituci?n (lunes)\n");
    printf("  - 17 de marzo: Natalicio de Benito Ju?rez (lunes)\n");
    printf("  - 17 de abril: Jueves Santo\n");
    printf("  - 18 de abril: Viernes Santo\n");
    printf("  - 1 de mayo: D?a del Trabajo\n");
    printf("  - 16 de septiembre: D?a de la Independencia\n");
    printf("  - 17 de noviembre: D?a de la Revoluci?n (lunes)\n");
    printf("  - 25 de diciembre: Navidad\n\n");
    printf("Regresando al men? principal...\n\n");
    
    while (getchar() != '\n'); // Espera que el usuario presione Enter
    getchar();
    return;
}

		
        // Selecci?n de horario
        printf("\nSeleccione el horario de entrada:\n");
        printf("1. 09:00 - 12:00\n");
        printf("2. 13:00 - 16:00\n");
        printf("3. 17:00 - 20:00\n");
        printf("Opci?n: ");
        scanf("%d", &opcion);

        switch (opcion) {
            case 1: strcpy(compra.horario, "09:00 - 12:00"); break;
            case 2: strcpy(compra.horario, "13:00 - 16:00"); break;
            case 3: strcpy(compra.horario, "17:00 - 20:00"); break;
            default: 
               printf("Opci?n inv?lida.\n"); return;
        }

        // Verificaci?n de capacidad
        int capacidadMaxima = 0;
        if (strcmp(compra.museo, "Museo de Louvre, Par?s") == 0) {
            capacidadMaxima = 5000;
        } else if (strcmp(compra.museo, "Museo Metropolitano de Nueva York") == 0) {
            capacidadMaxima = 3000;
        } else if (strcmp(compra.museo, "Museo Vaticano") == 0) {
            capacidadMaxima = 2000;
        } else if (strcmp(compra.museo, "Museo Nacional de Antropolog?a, Ciudad de M?xico") == 0) {
            capacidadMaxima = 1500;
        } else if (strcmp(compra.museo, "Museu Nacional d'Art de Catalunya") == 0) {
            capacidadMaxima = 1000;
        }

        printf("\nIngrese la cantidad de boletos a comprar (m?ximo 5): ");
        scanf("%d", &compra.cantidadBoletos);

        // Validaci?n de boletos
        if (compra.cantidadBoletos > 5) {
            printf("La cantidad m?xima de boletos es 5. Ajustando a 5 boletos.\n");
            compra.cantidadBoletos = 5;
        }
        if (compra.cantidadBoletos > capacidadMaxima) {
            printf("La cantidad de boletos excede la capacidad del museo (%d). Ajustando a la capacidad m?xima.\n", capacidadMaxima);
            compra.cantidadBoletos = capacidadMaxima;
        }

        // Datos de pago
        // Ingreso de datos de pago
    int metodoPago;

printf("\nElige el m?todo de pago:\n");
printf("1. Tarjeta de d?bito\n");
printf("2. Tarjeta de cr?dito\n");
printf("3. PayPal\n");
printf("Selecciona un m?todo de pago: ");
scanf("%d", &metodoPago); // Corregido: falta de '&'

switch (metodoPago) {
    case 1:
        strcpy(compra.metodoPago, "Tarjeta de d?bito");
        printf("Ingresa el n?mero de tarjeta (solo n?meros): ");
        scanf("%49s", compra.numeroTarjeta); // Limitar tama?o para evitar desbordamiento
        printf("Ingresa el nombre del titular: ");
        scanf(" %[^\n]", compra.nombrePago); // Leer nombres con espacios
        break;
    case 2:
        strcpy(compra.metodoPago, "Tarjeta de cr?dito");
        printf("Ingresa el n?mero de tarjeta (solo n?meros): ");
        scanf("%49s", compra.numeroTarjeta); // Limitar tama?o para evitar desbordamiento
        printf("Ingresa el nombre del titular: ");
        scanf(" %[^\n]", compra.nombrePago); // Leer nombres con espacios
        break;
    case 3:
        strcpy(compra.metodoPago, "PayPal");
        printf("Ingresa el correo electr?nico asociado a PayPal: ");
        scanf("%49s", compra.numeroTarjeta); // Considerar un campo separado para correos
        printf("Ingresa el nombre del titular: ");
        scanf(" %[^\n]", compra.nombrePago); // Leer nombres con espacios
        break;
    default:
        printf("Opci?n inv?lida.\n");
        return;
}


        // Mostrar restricciones
        printf("\n--- Restricciones ---\n");
        if (strcmp(compra.museo, "Museo de Louvre, Par?s") == 0) {
            printf("No se permite la entrada con mochilas grandes ni c?maras profesionales.\n");
        } else if (strcmp(compra.museo, "Museo Metropolitano de Nueva York") == 0) {
            printf("No se permite la entrada con alimentos o bebidas.\n");
        } else if (strcmp(compra.museo, "Museo Vaticano") == 0) {
            printf("Los visitantes deben vestir ropa apropiada (no se permite ropa corta o escotada).\n");
        } else if (strcmp(compra.museo, "Museo Nacional de Antropolog?a, Ciudad de M?xico") == 0) {
            printf("No se permiten c?maras en ciertas exhibiciones.\n");
        } else if (strcmp(compra.museo, "Museu Nacional d'Art de Catalunya") == 0) {
            printf("No se permite la entrada con grandes bolsas ni c?maras de video.\n");
        }
        printf("---------------------\n");

        // Calcular el precio
        compra.precio = 20.00 * compra.cantidadBoletos; // Precio por boleto

        // Mostrar detalles de la compra
        printf("\n--- Detalles de la Compra ---\n");
        printf("Museo: %s\n", compra.museo);
        printf("Fecha: %02d/%02d/%d\n", dia, mes, anio);
        printf("Horario: %s\n", compra.horario);
        printf("Cantidad de Boletos: %d\n", compra.cantidadBoletos);
        printf("Precio Total: %.2f\n", compra.precio);
        printf("M?todo de pago: %s\n", compra.metodoPago);
    if (strcmp(compra.metodoPago, "PayPal") == 0) {
        printf("Correo asociado: %s\n", compra.numeroTarjeta);
        printf("Titular: %s\n", compra.nombrePago);
    } else {
        printf("N?mero de tarjeta: %s\n", compra.numeroTarjeta);
        printf("Titular: %s\n", compra.nombrePago);
    }

        // Preguntar si desea realizar otra compra
        printf("\n?Desea realizar otra compra? (s/n): ");
        scanf(" %c", &continuar);
        limpiarPantalla();
    } while (continuar == 's');
}

#define MAX_USERS 100

// Estructura para guardar usuarios y contraseñas
typedef struct {
    char username[50];
    char password[50];
} Usuario;

// Función para validar si la cadena tiene solo minúsculas
int esMinusculas(const char *cadena) {
    for (int i = 0; cadena[i] != '\0'; i++) {
        if (!islower(cadena[i]) && !ispunct(cadena[i])) {
            return 0; // No es minúscula
        }
    }
    return 1; // Todo está en minúsculas
}

// Función para validar que los caracteres especiales estén al inicio o al final
int caracteresEspecialesValidos(const char *cadena) {
    int longitud = strlen(cadena);

    // Si la cadena tiene un carácter especial al inicio o al final, es válida
    if (ispunct(cadena[0]) || ispunct(cadena[longitud - 1])) {
        for (int i = 1; i < longitud - 1; i++) {
            if (ispunct(cadena[i])) {
                return 0; // No debe haber caracteres especiales en el medio
            }
        }
        return 1; // Es válido
    }

    // Si no tiene caracteres especiales, también es válido
    return 1;
}

// Función para validar que no haya números
int noTieneNumeros(const char *cadena) {
    for (int i = 0; cadena[i] != '\0'; i++) {
        if (isdigit(cadena[i])) {
            return 0; // Tiene números
        }
    }
    return 1; // No tiene números
}

// Función para registrar un usuario
int registrarUsuario(Usuario usuarios[], int *numUsuarios) {
    char nuevoUsuario[50];
    char nuevaContrasena[50];

    printf("\n===== Registro de Usuario =====\n");

    // Pedir nombre de usuario
    printf("Nuevo Usuario: ");
    scanf("%s", nuevoUsuario);

    // Validar usuario
    if (!esMinusculas(nuevoUsuario)) {
        printf("Error: El usuario debe contener solo letras minúsculas.\n");
        return 0;
    }
    if (!caracteresEspecialesValidos(nuevoUsuario)) {
        printf("Error: El usuario debe tener caracteres especiales solo al inicio o al final (o ninguno).\n");
        return 0;
    }
    if (!noTieneNumeros(nuevoUsuario)) {
        printf("Error: El usuario no debe contener números.\n");
        return 0;
    }

    // Pedir contraseña
    printf("Nueva Contraseña: ");
    scanf("%s", nuevaContrasena);

    // Validar contraseña
    if (!esMinusculas(nuevaContrasena)) {
        printf("Error: La contraseña debe contener solo letras minúsculas.\n");
        return 0;
    }
    if (!caracteresEspecialesValidos(nuevaContrasena)) {
        printf("Error: La contraseña debe tener caracteres especiales solo al inicio o al final.\n");
        return 0;
    }
    if (!noTieneNumeros(nuevaContrasena)) {
        printf("Error: La contraseña no debe contener números.\n");
        return 0;
    }

    // Guardar usuario y contraseña
    strcpy(usuarios[*numUsuarios].username, nuevoUsuario);
    strcpy(usuarios[*numUsuarios].password, nuevaContrasena);
    (*numUsuarios)++;

    printf("Registro exitoso. ¡Ahora puedes iniciar sesión!\n");
    return 1;
}

// Función para iniciar sesión
void iniciarSesion(Usuario usuarios[], int numUsuarios) {
    char inputUsername[50];
    char inputPassword[50];
    int loginSuccess = 0;

    printf("\n===== Iniciar Sesión =====\n");

    while (!loginSuccess) {
        // Pedir nombre de usuario
        printf("Usuario: ");
        scanf("%s", inputUsername);

        // Pedir contraseña
        printf("Contraseña: ");
        scanf("%s", inputPassword);

        // Verificar credenciales
        for (int i = 0; i < numUsuarios; i++) {
            if (strcmp(inputUsername, usuarios[i].username) == 0 &&
                strcmp(inputPassword, usuarios[i].password) == 0) {
                printf("Inicio de sesión exitoso. ¡Bienvenido, %s!\n", inputUsername);
                loginSuccess = 1;
            
            }
        }

        if (!loginSuccess) {
            printf("Credenciales incorrectas. Por favor, inténtalo de nuevo.\n");
        }
    }
}

int main() {
    int opcion;
    
    Usuario usuarios[MAX_USERS];
    int numUsuarios = 0;

    printf("===== Sistema de TicketMaster =====\n");

    do {
        // Menú principal
        printf("\n1. Registrarse\n");
        printf("2. Iniciar sesión\n");
        printf("3. Salir\n");
        printf("Selecciona una opción: ");
        scanf("%d", &opcion);

        switch (opcion) {
            case 1:
                registrarUsuario(usuarios, &numUsuarios);
                break;
            case 2:
                if (numUsuarios == 0) {
                    printf("No hay usuarios registrados. Por favor, regístrate primero.\n");
                } else {
                    iniciarSesion(usuarios, numUsuarios);
                     do {
    	// Datos del estudiante
    	printf("\n\n");
    printf("\n****TICKETMASTER*****\n\n");
    printf("Estudiante: Cristopher");
    printf("C?digo: 221960314");

    // Horarios de servicio y d?as festivos al inicio
    printf("\n--- Horarios de servicio ---\n");
    printf("Horarios de servicio: Lunes a Viernes, 10:00 - 20:00\n");
    printf("No se pueden adquirir boletos en d?as no laborales.\n");

    printf("\n\nNo es posible comprar boletos en d?as festivos.\n");
    printf("Estos son los d?as festivos de 2025 en M?xico:\n");
    printf("  - 1 de enero: A?o Nuevo\n");
    printf("  - 3 de febrero: D?a de la Constituci?n (lunes)\n");
    printf("  - 17 de marzo: Natalicio de Benito Ju?rez (lunes)\n");
    printf("  - 17 de abril: Jueves Santo\n");
    printf("  - 18 de abril: Viernes Santo\n");
    printf("  - 1 de mayo: D?a del Trabajo\n");
    printf("  - 16 de septiembre: D?a de la Independencia\n");
    printf("  - 17 de noviembre: D?a de la Revoluci?n (lunes)\n");
    printf("  - 25 de diciembre: Navidad\n\n");

    
        // Mostrar men? de opciones
        printf("\n----- MEN? -----\n");
        printf("1. Teatro\n");
        printf("2. Cine\n");
        printf("3. Museo\n");
        printf("4. Salir\n");
        printf("Selecciona una opci?n: ");
        scanf("%d", &opcion);

        // Opciones del men?
        switch (opcion) {
            case 1:
                elegirTeatro();  // Funci?n para seleccionar el teatro
                break;
            case 2:
                elegirCine();
                break;
            case 3:
                elegirMuseo();
                break;
            case 4:
                printf("Saliendo...\n");
                break;
            default:
                printf("Opci?n inv?lida.\n");
                break;
    		}
	}while (opcion != 4);
                }
                break;
            case 3:
                printf("Saliendo del sistema. ¡Hasta luego!\n");
                break;
            default:
                printf("Opción no válida. Inténtalo de nuevo.\n");
        }
    } while (opcion != 3);

	

    return 0;
	}

