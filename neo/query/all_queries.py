Industry_Gdp_Query = """
SELECT 
    Curr.year as Year,Curr.iname as Industry_Name,
    Gdp_per_year.Total_Gdp as Total_Gdp,
    (Curr.Total_Annual_Pay - Prev.Total_Annual_Pay)/Prev.Total_Annual_Pay * 100 as Growth
FROM
    (SELECT
        G1.year as year,
        SUM(DISTINCT G1.real_gdp) as Total_Gdp
    FROM
        "HARSHITH.KUMAR".Gdp G1
    JOIN
        "HARSHITH.KUMAR".County_Fips CF1
    ON
        G1.county_fips = CF1.fips
    JOIN 
        "HARSHITH.KUMAR".State S
    ON
        CF1.state_fips = S.fips
    WHERE S.Name = CASE WHEN '{state}' = 'all' THEN S.Name ELSE '{state}' END
    GROUP BY
        G1.year
    ) Gdp_per_year
JOIN 
    (SELECT
        G1.year as year,
        IC1.industry_name as iname,
        SUM(G1.real_gdp) as Total_Gdp,
        SUM(I1.Annual_Pay) as Total_Annual_Pay
    FROM
        "HARSHITH.KUMAR".Gdp G1
    JOIN
        "HARSHITH.KUMAR".County_Fips CF1
    ON
        G1.county_fips = CF1.fips
    JOIN 
        "HARSHITH.KUMAR".State S1
    ON
        CF1.state_fips = S1.fips
    JOIN
        "HARSHITH.KUMAR".Industry I1
    ON
        I1.year = G1.year AND
        I1.county_fips = CF1.fips
    JOIN
        "HARSHITH.KUMAR".Industry_Category IC1
    ON
        IC1.naics = I1.naics
    WHERE S1.Name = CASE WHEN '{state}' = 'all' THEN S1.Name ELSE '{state}' END AND
    IC1.naics IN ({bind_industries}) AND
    I1.year >= {start_year} AND
    I1.year <= {end_year}
    GROUP BY
        G1.year, IC1.Industry_Name
) CURR
ON Gdp_per_year.year = CURR.year
JOIN (
    SELECT 
        I2.year as year, IC2.industry_name as iname, 
        SUM(I2.Annual_Pay) as Total_Annual_Pay
    FROM
        "HARSHITH.KUMAR".Industry I2
    JOIN
        "HARSHITH.KUMAR".County_Fips CF2
    ON
        I2.county_fips = CF2.fips
    JOIN
        "HARSHITH.KUMAR".State S2
    ON
        S2.fips = CF2.state_fips
    JOIN
        "HARSHITH.KUMAR".Industry_Category IC2
    ON
        I2.naics = IC2.naics
    WHERE S2.Name = CASE WHEN '{state}' = 'all' THEN S2.Name ELSE '{state}' END
    GROUP BY
        I2.year, IC2.industry_name
    ) PREV
ON 
    CURR.year = PREV.year+1 AND
    CURR.iname = PREV.iname
ORDER BY CURR.year ASC
"""

Homelessness_Mortgage_Query = """
SELECT 
    year, 
    AVG(thirty_year_frm) AS thirty_year_frm, 
    total_homelessness_rate, 
    total_caucasian_homelessness_rate, 
    total_african_american_homelessness_rate, 
    total_american_indian_homelessness_rate, 
    total_asian_american_homelessness_rate, 
    total_hawaiian_homelessness_rate, 
    total_hispanic_homelessness_rate
FROM "HARSHITH.KUMAR".MORTGAGE NATURAL JOIN (
    SELECT 
        year, 
        ((SUM(overall_homeless_male) + SUM(overall_homeless_female))/total_state_population) * 1000 AS total_homelessness_rate,
        (SUM(caucasian)/total_caucasian) * 1000 AS total_caucasian_homelessness_rate,
        (SUM(african_american)/total_african_american) * 1000 AS total_african_american_homelessness_rate,
        (SUM(american_indian)/total_american_indian) * 1000 AS total_american_indian_homelessness_rate,
        (SUM(asian_american)/total_asian_american) * 1000 AS total_asian_american_homelessness_rate,
        (SUM(hawaiian)/total_hawaiian) * 1000 AS total_hawaiian_homelessness_rate,
        (SUM(hispanic_latino)/total_hispanic) * 1000 AS total_hispanic_homelessness_rate
    FROM "HARSHITH.KUMAR".HOMELESSNESS NATURAL JOIN (
        SELECT 
            year, 
            state_fips, 
            SUM(caucasian) AS total_caucasian,
            SUM(african_american) AS total_african_american,
            SUM(american_indian) AS total_american_indian,
            SUM(asian_american) AS total_asian_american,
            SUM(hawaiian) AS total_hawaiian,
            SUM(hispanic) AS total_hispanic,
            SUM(population) AS total_state_population
        FROM "HARSHITH.KUMAR".DEMOGRAPHIC NATURAL JOIN (
            SELECT 
                year, 
                state_fips, 
                fips AS county_fips, 
                population
            FROM "HARSHITH.KUMAR".COUNTY NATURAL JOIN (
                SELECT 
                    state_fips, 
                    fips 
                FROM "HARSHITH.KUMAR".COUNTY_FIPS NATURAL JOIN (
                    SELECT 
                        fips AS state_fips
                    FROM "HARSHITH.KUMAR".STATE
                    WHERE name = '{state}'
                )
            )
        ) GROUP BY 
            year, 
            state_fips
    )GROUP BY 
        year, 
        state_fips, 
        total_state_population, 
        total_caucasian, 
        total_african_american, 
        total_american_indian, 
        total_asian_american, 
        total_hawaiian, 
        total_hispanic
) WHERE year >= {start_year} AND year <= {end_year}
GROUP BY 
    year, 
    total_homelessness_rate, 
    total_caucasian_homelessness_rate, 
    total_african_american_homelessness_rate, 
    total_american_indian_homelessness_rate, 
    total_asian_american_homelessness_rate, 
    total_hawaiian_homelessness_rate, 
    total_hispanic_homelessness_rate
ORDER BY year ASC
"""

Crime_Unemployment_Query = """
SELECT
    S1.name AS State_Name,
    c1.year AS year,
    ROUND(AVG(((c1.murder)/d1.total) *10000),2) AS murder_rate_per_year,
    ROUND(AVG(((c1.rape)/d1.total) *10000),2) AS rape_rate_per_year,
    ROUND(AVG(((c1.robbery)/d1.total) *10000),2) AS robbery_rate_per_year,
    ROUND(AVG(((c1.aggravated_assault)/d1.total) *10000),2) AS aggravated_assault_rate_per_year,
    ROUND(AVG(((c1.burglary)/d1.total) *10000),2) AS burglary_rate_per_year,
    ROUND(AVG(((c1.larceny)/d1.total) *10000),2) AS larceny_rate_per_year,
    ROUND(AVG(((c1.motor_vechile_theft)/d1.total) *10000),2) AS motor_vechile_theft_rate_per_year,
    ROUND(AVG(((c1.arson)/d1.total) *10000),2) AS arson_rate_per_year,
    ROUND(AVG(((c1.murder + c1.rape + c1.robbery + c1.aggravated_assault + c1.burglary + c1.larceny + c1.motor_vechile_theft + c1.arson)/d1.total) *1000),2) AS crime_rate_per_year,
    SUM(c1.murder + c1.rape + c1.robbery + c1.aggravated_assault) AS total_violent_crime_year,
    SUM(c1.burglary + c1.larceny + c1.motor_vechile_theft + c1.arson) AS total_non_violent_crime_year,
    ROUND(AVG((u1.unemployed / (u1.employed + u1.unemployed)) * 100),2) AS unemployment_rate_per_year
    FROM
        "HARSHITH.KUMAR".Crime c1
    JOIN
        "HARSHITH.KUMAR".Unemployment u1
    ON
        c1.county_fips = u1.county_fips AND
        c1.year = u1.year
    JOIN
        "HARSHITH.KUMAR".Demographic d1
    ON
        u1.county_fips = d1.county_fips AND
        u1.year = d1.year
    JOIN
        "HARSHITH.KUMAR".County_fips cf1
    ON
        d1.county_fips = cf1.fips
    JOIN 
        "HARSHITH.KUMAR".state s1
    ON
        cf1.state_fips = s1.fips
    WHERE 
        s1.name IN ({bind_states}) AND
        c1.year >= {start_year} AND
        c1.year <= {end_year}
    GROUP BY 
        c1.year, 
        s1.name
    ORDER BY
        c1.year
"""

Crime_Unemployment_Query_Overall = """
SELECT
    s.name AS state_name,
    ROUND(AVG(((c.murder)/d.total) *10000),2) AS total_murder_rate_05_19,
    ROUND(AVG(((c.rape)/d.total) *10000),2) AS total_rape_rate_05_19,
    ROUND(AVG(((c.robbery)/d.total) *10000),2) AS total_robbery_rate_05_19,
    ROUND(AVG(((c.aggravated_assault)/d.total) *10000),2) AS total_aggravated_assault_rate_05_19,
    ROUND(AVG(((c.burglary)/d.total) *10000),2) AS total_burglary_rate_05_19,
    ROUND(AVG(((c.larceny)/d.total) *10000),2) AS total_larceny_rate_05_19,
    ROUND(AVG(((c.motor_vechile_theft)/d.total) *10000),2) AS total_motor_vechile_theft_rate_05_19,
    ROUND(AVG(((c.arson)/d.total) *10000),2) AS total_arson_rate_05_19,
    ROUND(AVG(((c.murder + c.rape + c.robbery + c.aggravated_assault + c.burglary + c.larceny + c.motor_vechile_theft + c.arson)/d.total) *1000),2) AS total_crime_rate_05_19,
    ROUND(AVG((u.unemployed / (u.employed + u.unemployed)) * 100), 2) AS total_unemployment_rate_05_19
FROM 
    "HARSHITH.KUMAR".crime c
JOIN 
    "HARSHITH.KUMAR".unemployment u ON c.county_fips = u.county_fips AND c.year = u.year
JOIN 
    "HARSHITH.KUMAR".demographic d ON c.county_fips = d.county_fips AND c.year = d.year
JOIN 
    "HARSHITH.KUMAR".county_fips cf ON c.county_fips = cf.fips
JOIN 
    "HARSHITH.KUMAR".state s ON cf.state_fips = s.fips
WHERE 
    s.name IN ({bind_states})
GROUP BY 
    s.name
"""

Poverty_Demographics_Query = """

    SELECT 
    Demo_T.Year,Demo_T.State_Name,
    Demo_T.State_Code,
    Demo_T.Total_Population,
    Demo_T.total_african_american_population_percentage,
    Demo_T.total_american_indian_population_percentage,
    Demo_T.total_caucasian_population_percentage,
    Demo_T.total_asian_american_population_percentage,
    Demo_T.total_hawaiian_population_percentage,
    Demo_T.total_hispanic_population_percentage,
    Demo_T.total_non_hispanic_population_percentage,
    Poverty_T.total_poverty,
    ROUND((Poverty_T.total_poverty / Demo_T.total_population)*100,2) as total_poverty_percentage,
    Poverty_T.total_poverty_under_18,
    ROUND((Poverty_T.total_poverty_under_18 / Demo_T.total_population_under_18)*100,2) as total_poverty_under_18_percentage,
    Poverty_T.total_poverty_over_18,
    ROUND((Poverty_T.total_poverty_over_18 / Demo_T.total_population_over_18)*100,2) as total_poverty_over_18_percentage,
    Poverty_T.Average_HouseHold_Income
    FROM (
         ( SELECT P.year as year,S.name as State_Name,S.Fips as State_Code,
            SUM(P.poverty_estimate_all) as total_poverty,
            SUM(P.poverty_estimate_age_0_17) as total_poverty_under_18,
            SUM((P.poverty_estimate_all - P.poverty_estimate_age_0_17)) as total_poverty_over_18,
            ROUND(AVG(P.median_household_income),2) as Average_HouseHold_Income 
            FROM 
                "HARSHITH.KUMAR".Poverty P
            INNER JOIN 
                 "HARSHITH.KUMAR".County_Fips CF
            ON 
                P.county_fips = CF.fips
            INNER JOIN 
                "HARSHITH.KUMAR".State S
            ON
                S.fips = CF.state_fips  
            GROUP BY
                    S.fips,P.year,S.name
            ORDER BY 
                   P.year,S.name  
            ) Poverty_T
            INNER JOIN
                ( SELECT Demo.year as year,S.name as State_Name,S.fips as State_Code,
                    SUM(Demo.total) as total_population,
                    SUM(Demo.overall_0_4 + Demo.overall_5_17) AS total_population_under_18,
                    SUM(Demo.overall_18_24 + Demo.overall_25_44 + Demo.overall_45_64 + Demo.overall_65) as total_population_over_18,
                    ROUND(SUM(Demo.african_american)/SUM(Demo.total)*100,2) as total_african_american_population_percentage,
                    ROUND(SUM(Demo.american_indian)/SUM(Demo.total)*100,2) as total_american_indian_population_percentage,
                    
                    ROUND(SUM(Demo.caucasian)/SUM(Demo.total)*100,2) as total_caucasian_population_percentage,
                    ROUND(SUM(Demo.asian_american)/SUM(Demo.total)*100,2) as total_asian_american_population_percentage,
                    ROUND(SUM(Demo.hawaiian)/SUM(Demo.total)*100,2) as total_hawaiian_population_percentage,
                    ROUND(SUM(Demo.hispanic)/SUM(Demo.total)*100,2) as total_hispanic_population_percentage,
                    ROUND(SUM(Demo.non_hispanic)/SUM(Demo.total)*100,2) as total_non_hispanic_population_percentage
                    FROM
                        "HARSHITH.KUMAR".Demographic Demo    
                    INNER JOIN 
                        "HARSHITH.KUMAR".County_Fips CF
                    ON 
                        Demo.county_fips = CF.fips
                    INNER JOIN 
                        "HARSHITH.KUMAR".State S
                    ON
                        S.fips = CF.state_fips
                        
                    GROUP BY
                        Demo.year,S.name,S.fips
                    ORDER BY 
                        Demo.year,S.name  
                ) DEMO_T
            ON Poverty_T.State_Name = Demo_T.State_Name AND Poverty_T.State_Code = Demo_T.State_Code AND Poverty_T.year = Demo_T.year          
    ) WHERE Demo_T.State_Name = '{state}' AND Demo_T.year >= {start_year} AND Demo_T.year <= {end_year}


"""