aircond_alix_sadosky
==============================

Introducción
---------------
Les presentamos a la empresa “Frío Frío”, dedicada a la venta e instalación de equipos de aire acondicionado para grandes superficies. Al ser una empresa B2B (“Business To Business”), es esencial para ellos optimizar los esfuerzos de los representantes comerciales, ayudándolos a priorizar las oportunidades en el pipeline.

Una “oportunidad” consiste en un proyecto de venta o instalación de equipos para un cliente. La venta se estructura alrededor de TRF (Toneladas de refrigeración) y puede estar compuesta por varios productos distintos. El "pipeline" hace referencia al flujo de oportunidades prospecto que la empresa está desarrollando. El equipo comercial asigna a distintos momentos, para cada oportunidad, un estado en la negociación. En la Ilustración se muestran los estados que las oportunidades tienen dentro del pipeline.

La variable que se está tratando de predecir es “Probabilidad de éxito” para cada oportunidad. ¿Cuál es la probabilidad de que la oportunidad se convierta en un caso Closed Won?
El dataset cuenta con información de cada oportunidad, como por ejemplo información sobre el vendedor a cargo de la venta, información geográfica de los clientes, TRS pedidas, fecha prevista de entrega de los equipos, etc. A partir de dichas variables es posible entrenar un modelo que prediga para un tiempo futuro el éxito o fracaso de cada oportunidad. Idealmente, “Frío Frío” podrá usar este modelo para predecir la probabilidad de éxito de cada oportunidad comercial, para mejorar el rendimiento y optimizar el esfuerzo de los vendedores.

El objetivo de esta competencia es, en base a los datos de oportunidades históricas, predecir el éxito de todas las oportunidade comerciales surgidas en los últimos cuatro meses.

Recuerden que para estar inscriptos en la competencia deben hacer por lo menos 1 submit, les recomendamos utilizar el archivo de prueba para ese fin.



## Descripción
#### Diccionario de variables

- ID: id único del registro (Entero).
- Región: región de la oportunidad (Categórica).
- Territory: territorio comercial de la oportunidad (Categórica).
- Pricing, Delivery_Terms_Quote_Approval: variable que denomina si la oportunidad necesita aprobación especial de su precio total y los términos de la entrega (Binaria).
- Pricing, Delivery_Terms_Approved: variable que denomina si la oportunidad obtuvo aprobación especial de su precio total y los términos de la entrega (Binaria).
- Bureaucratic_Code_0_Approval: variable que denomina si la oportunidad necesita el código burocrático 0 (Binaria).
- Bureaucratic_Code_0_Approved: variable que denomina si la oportunidad obtuvo el código burocrático 0 (Binaria).
- Submitted_for_Approval: variable que denomina si fue entregada la oportunidad para la aprobación (Binaria).
- Bureaucratic_Code: códigos burocráticos que obtuvo la oportunidad (Categórica).
- Account_Created_Date: fecha de creación de la cuenta del cliente (Datetime).
- Source: fuente de creación de la oportunidad (Categórica).
- Billing_Country: país donde se emite la factura (Categórica).
- Account_Name: nombre de la cuenta del cliente (Categórica).
- Opportunity_Name: nombre de la oportunidad (Categórica).
- Opportunity_ID: id de la oportunidad (Entero).
- Sales_Contract_No: número de contrato (Entero).
- Account_Owner: vendedor del equipo comercial responsable de la cuenta cliente (Categórica).
- Opportunity_Owner: vendedor del equipo comercial responsable de la oportunidad comercial (Categórica).
- Account_Type: tipo de cuenta cliente (Categórica).
- Opportunity_Type: tipo de oportunidad (Categórica).
- Quote_Type: tipo de presupuesto (Categórica).
- Delivery_Terms: términos de entrega (Categórica).
- Opportunity_Created_Date: fecha de creación de la oportunidad comercial (Datetime).
- Brand: marca del producto (Categórica).
- Product_Type: tipo de producto (Categórica).
- Size: tamaño del producto (Categórica).
- Product_Category_B: categoría 'B' del producto (Categórica).
- Price: precio (Decimal).
- Currency: moneda (Categórica).
- Last_Activity: fecha de la última actividad (Datetime).
- Quote_Expiry_Date: fecha de vencimiento del presupuesto (Datetime).
- Last_Modified_Date: fecha de ultima modificación en la oportunidad (Datetime).
- Last_Modified_By: usuario responsable de la última modificación en la oportunidad (Categórica).
- Product_Family: familia de producto (Categórica).
- Product_Name: nombre del producto (Categórica).
- ASP_Currency: moneda del precio promedio (Categórica).
- ASP: (Average Selling Price) precio promedio a la venta (Decimal).
- ASP_(converted)_Currency: moneda del precio promedio convertido en la variable (Categórica)
- ASP_(converted): precio promedio a la venta convertido a otra moneda (Decimal).
- Planned_Delivery_Start_Date: límite inferior del rango previsto para la fecha de entrega (Datetime).
- Planned_Delivery_End_Date: límite superior del rango previsto para la fecha de entrega (Datetime).
- Month: mes-año de Planned_Delivery_Start_Date (Fecha).
- Delivery_Quarter: trimestre de Planned_Delivery_Start_Date (Categorica).
- Delivery_Year: año de Planned_Delivery_Start_Date (Fecha).
- Actual_Delivery_Date: fecha real de la entrega (Datetime).
- Total_Power: potencia del producto (Entero).
- Total_Amount_Currency: moneda del monto total (Decimal).
- Total_Amount: monto total (Decimal).
- Total_Taxable_Amount_Currency: moneda del monto gravado total (Categórica).
- Total_Taxable_Amount: monto gravado total (Categórica).
- Stage: variable target. Estado de la oportunidad (Categórica).
- Prod_Category_A: categoría 'A' del producto (Categórica).
- Total_Power_Discreet: categorización de la variable Total Power en bins (Categórica).