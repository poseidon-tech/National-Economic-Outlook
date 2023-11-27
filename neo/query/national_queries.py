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