Industry_Gdp_Query = """
SELECT 
    Curr.year as Year,Curr.iname as Industry_Name,
    Curr.State_Name as State,
    Gdp_per_year.Total_Gdp as Total_Gdp,
    (Curr.Total_Annual_Pay - Prev.Total_Annual_Pay)/Prev.Total_Annual_Pay * 100 as Growth
    FROM
        (SELECT
            G1.year as year,
            S.Name as State_Name,
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
        GROUP BY
            G1.year, S.name
        ) Gdp_per_year
    JOIN 
        (SELECT
            G1.year as year,
            IC1.industry_name as iname,
            S1.Name as State_Name,
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
        WHERE S1.Name IN ({bind_states}) AND
        IC1.naics IN ({bind_industries}) AND
        I1.year >= {start_year} AND
        I1.year <= {end_year}
        GROUP BY
            G1.year, IC1.Industry_Name, S1.name
    ) CURR
    ON Gdp_per_year.year = CURR.year
    AND Gdp_per_year.State_Name = CURR.State_Name
    JOIN (
        SELECT 
            I2.year as year, IC2.industry_name as iname, 
            SUM(I2.Annual_Pay) as Total_Annual_Pay,
            S2.name as State_Name
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
        GROUP BY
            I2.year, IC2.industry_name, S2.name
        ) PREV
    ON 
        CURR.year = PREV.year+1 AND
        CURR.iname = PREV.iname AND
        CURR.State_Name = PREV.State_Name
ORDER BY CURR.year ASC
"""
