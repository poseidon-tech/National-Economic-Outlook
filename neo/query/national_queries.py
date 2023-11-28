National_Homelessness_Mortgage_Query = """
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
        ((SUM(overall_homeless_male) + SUM(overall_homeless_female))/total_population) * 1000 AS total_homelessness_rate,
        (SUM(caucasian)/total_caucasian) * 1000 AS total_caucasian_homelessness_rate,
        (SUM(african_american)/total_african_american) * 1000 AS total_african_american_homelessness_rate,
        (SUM(american_indian)/total_american_indian) * 1000 AS total_american_indian_homelessness_rate,
        (SUM(asian_american)/total_asian_american) * 1000 AS total_asian_american_homelessness_rate,
        (SUM(hawaiian)/total_hawaiian) * 1000 AS total_hawaiian_homelessness_rate,
        (SUM(hispanic_latino)/total_hispanic) * 1000 AS total_hispanic_homelessness_rate
    FROM "HARSHITH.KUMAR".HOMELESSNESS NATURAL JOIN (
        SELECT 
            year, 
            SUM(caucasian) AS total_caucasian,
            SUM(african_american) AS total_african_american,
            SUM(american_indian) AS total_american_indian,
            SUM(asian_american) AS total_asian_american,
            SUM(hawaiian) AS total_hawaiian,
            SUM(hispanic) AS total_hispanic,
            SUM(population) AS total_population
        FROM "HARSHITH.KUMAR".DEMOGRAPHIC NATURAL JOIN (
            SELECT 
                year, 
                fips AS county_fips, 
                population
            FROM "HARSHITH.KUMAR".COUNTY NATURAL JOIN (
                SELECT 
                    fips 
                FROM "HARSHITH.KUMAR".COUNTY_FIPS NATURAL JOIN (
                    SELECT 
                        fips AS state_fips
                    FROM "HARSHITH.KUMAR".STATE
                )
            )
        ) GROUP BY 
            year
    )GROUP BY 
        year, 
        total_population, 
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

National_Poverty_Demographic_Query = """

SELECT 
    Demo_T.Year,
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
         ( SELECT P.year as year,
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
            GROUP BY
                    P.year
            ORDER BY 
                   P.year
            ) Poverty_T
            INNER JOIN
                ( SELECT Demo.year as year,
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

                    GROUP BY
                        Demo.year
                    ORDER BY 
                        Demo.year
                ) DEMO_T
            ON Poverty_T.year = Demo_T.year          
    )
    


"""