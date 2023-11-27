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

Crime_Unemployment_Query = """
WITH state_crime_overall AS (SELECT
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
GROUP BY 
    s.name
)
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
    ROUND(AVG((u1.unemployed / (u1.employed + u1.unemployed)) * 100),2) AS unemployment_rate_per_year,
    total_murder_rate_05_19 AS murder_rate_frm_2005_2019,
    total_rape_rate_05_19 AS rape_rate_frm_2005_2019,
    total_robbery_rate_05_19 AS robbery_rate_frm_2005_2019,
    total_aggravated_assault_rate_05_19 AS aggravated_assault_rate_frm_2005_2019,
    total_burglary_rate_05_19 AS burglary_rate_frm_2005_2019,
    total_larceny_rate_05_19 AS larceny_rate_frm_2005_2019,
    total_motor_vechile_theft_rate_05_19 AS motor_vechile_theft_rate_frm_2005_2019,
    total_arson_rate_05_19 AS arson_rate_frm_2005_2019,
    total_crime_rate_05_19 AS crime_rate_frm_2005_2019,
    total_unemployment_rate_05_19 AS unemployment_rate_frm_2005_2019
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
    JOIN 
        state_crime_overall sc
    ON 
        s1.name = sc.state_name
    WHERE 
        s1.name IN({bind_states}) AND
        c1.year >= {start_year} AND
        c1.year <= {end_year}
    GROUP BY 
        c1.year, 
        s1.name,
        total_murder_rate_05_19,
        total_rape_rate_05_19,
        total_robbery_rate_05_19,
        total_aggravated_assault_rate_05_19,
        total_burglary_rate_05_19,
        total_larceny_rate_05_19,
        total_motor_vechile_theft_rate_05_19,
        total_arson_rate_05_19,
        total_crime_rate_05_19,
        total_unemployment_rate_05_19
    ORDER BY
        c1.year
"""
