class SqlQueries:


    # Create staging table   
    staging_review_table_create = ("""
        CREATE TABLE public.staging_review (
        review_id VARCHAR(255) not null, 
        user_id VARCHAR(255) not null,
        business_id VARCHAR(255) not null,
        date VARCHAR(255) NOT NULL,
        stars FLOAT4,
        useful INT,
        funny INT,
        cool INT
        );
    """)

    staging_tip_table_create = ("""
        CREATE TABLE public.staging_tip (
        user_id VARCHAR(255), 
        business_id VARCHAR(255),
        date VARCHAR(255),
        compliment_count INT
        )
    """)

    staging_users_table_create = ("""
        CREATE TABLE public.staging_user (
        user_id varchar(255) NOT NULL,
        name varchar(255) NOT NULL,
        review_count INT,
        yelping_since varchar(255),
        useful INT,
        funny INT,
        cool INT,
        fans INT,
        average_stars FLOAT4
    )
    """)

    staging_business_table_create = ("""
        CREATE TABLE public.staging_business (
        business_id VARCHAR(255) not null, 
        name VARCHAR(255) not null, 
        address VARCHAR(255) not null,
        city VARCHAR(255) not null, 
        state VARCHAR(255) not null, 
        postal_code VARCHAR(255) not null,
        stars FLOAT4, 
        review_count INT, 
        is_open VARCHAR(255), 
        categories VARCHAR(65535)
        )
    """)

    staging_checkin_table_create = ("""
        CREATE TABLE public.staging_checkin (
        business_id	VARCHAR(255) not null, 
        date VARCHAR(255) not null
        )
    """)

    staging_cities_table_create = ("""
        CREATE TABLE public.staging_cities (
        city VARCHAR(255) not null, 
        state VARCHAR(255) not null,
        state_code VARCHAR(255) not null,
        avg_household_size FLOAT4,
        median_age FLOAT4, 
        male_population FLOAT4,
        female_population FLOAT4,
        total_population FLOAT4
        )
    """)

    # Create dimension tables  
    dimension_business_table_create = ("""
        CREATE TABLE public.dim_business(
        business_id VARCHAR(255) not null,
        name VARCHAR(255) not null,
        address VARCHAR(255) not null,
        stars FLOAT4, 
        review_count INT,
        is_open VARCHAR(255),
        categories VARCHAR(65535), 
        location_id VARCHAR(255) 
        )
    """) 

    dimension_cities_table_create = ("""
        CREATE TABLE public.dim_cities (
        city VARCHAR(255) not null, 
        state VARCHAR(255) not null,
        state_code VARCHAR(255) not null,
        avg_household_size FLOAT4,
        median_age FLOAT4, 
        male_population FLOAT4,
        female_population FLOAT4,
        total_population FLOAT4
        )
    """)

    dimension_location_table_create = ("""
        CREATE TABLE public.dim_business_location(
        location_id VARCHAR(255) not null,
        city VARCHAR(255) not null, 
        state VARCHAR(255) not null, 
        postal_code VARCHAR(255) NOT NULL 
        )
    """)

    dimension_users_table_create = ("""
        CREATE TABLE public.dim_users (
        user_id varchar(255) NOT NULL,
        name varchar(255) NOT NULL,
        yelping_since_ts TIMESTAMP NOT NULL,
        yelping_since_date DATE NOT NULL,
        review_count INT,
        useful INT,
        funny INT,
        cool INT,
        fans INT,
        average_stars FLOAT4
        )
    """)

    dimension_date_table_create = ("""
        CREATE public.dim_date AS 
        select 
            ('2020-01-01'::date + i)::timestamp AS dates, 
            extract(year from dates ) as year,
            extract( qtr  from  dates ) as quarter,
            extract(month from dates ) as month,
            extract(day from dates ) as day,
            to_char(dates, 'Day') as weekday_name,
            extract( yearday from dates ) as day_from_year_beginning 
        from 
            generate_series(0,datediff('day', '2020-01-01', getdate() )) as x 

        )
    """)




    # Insert dimension tables
    dimension_location_table_insert = ("""
        INSERT INTO public.dim_business_location(
        location_id,
        city, 
        state, 
        postal_code
        )
        
        SELECT 
            DISTINCT md5(city || state || postal_code) AS location_id, 
            city,
            state,
            postal_code
        FROM 
            public.staging_business
    """)

    dimension_business_table_insert = ("""
        INSERT INTO public.dim_business(
            business_id,
            name,
            address,
            stars,
            review_count,
            is_open, 
            categories,
            location_id
        )
        
        SELECT 
            sb.business_id,
            sb.name AS business_name,
            sb.address,
            sb.stars,
            sb.review_count,
            sb.is_open, 
            sb.categories,
            dl.location_id
        FROM 
            public.staging_business sb 
        LEFT JOIN dim_business_location dl ON sb.city = dl.city
            AND sb.state = dl.state
            AND sb.postal_code = dl.postal_code
    """)

    dimension_cities_table_insert = ("""
        INSERT INTO public.dim_cities(
            city, 
            state,
            state_code,
            avg_household_size,
            median_age, 
            male_population,
            female_population,
            total_population
        )
        
        SELECT 
            *
        FROM 
            public.staging_cities 

    """)

    dimension_users_table_insert = ("""
        INSERT INTO public.dim_users(
            user_id,
            name, 
            yelping_since_ts,
            yelping_since_date,
            review_count,
            useful,
            funny, 
            cool,
            fans, 
            average_stars
        )
        
        SELECT 
            su.user_id,
            su.name,
            to_timestamp(su.yelping_since, 'YYYY-MM-DD HH24:MI:SS') AS yelping_since_ts,
            to_date(su.yelping_since, 'YYYY-MM-DD') AS yelping_since_date,
            su.review_count::INT AS review_count,
            su.useful,
            su.funny, 
            su.cool,
            su.fans, 
            su.average_stars
        FROM 
            public.staging_user su 

    """)



    # Create fact tables
    fact_review_table_create = ("""
        CREATE TABLE public.fact_review (
        review_id VARCHAR(255) not null,
        user_id VARCHAR(255) not null,
        business_id VARCHAR(255) not null,
        review_ts TIMESTAMP NOT NULL,
        review_date DATE NOT NULL,
        stars FLOAT4,
        useful INT,
        funny INT,
        cool INT
        )
    """)

    fact_checkin_table_create = ("""
        CREATE TABLE public.fact_checkin (
        business_id	VARCHAR(255) NOT NULL, 
        checkin_ts TIMESTAMP NOT NULL,
        checkin_date DATE NOT NULL,
        year INT ,
        month INT,
        day INT,
        hour INT,
        minute INT 
        )
    """)

    fact_tip_table_create = ("""
        CREATE TABLE public.fact_tip (
        user_id VARCHAR(255), 
        business_id VARCHAR(255),
        tip_ts TIMESTAMP NOT NULL,
        tip_date DATE NOT NULL,
        tip_year INT,
        tip_month INT,
        tip_day INT,
        tip_hour INT,
        tip_minute INT,
        compliment_count INT
        )
    """)

    # Insert fact tables
    fact_review_table_insert = ("""
        INSERT INTO public.fact_review(
            review_id,
            user_id,
            business_id,
            review_ts,
            review_date, 
            stars,
            useful,
            funny, 
            cool
        )
        
        SELECT 
            sr.review_id,
            sr.user_id,
            sr.business_id,
            to_timestamp(sr.date, 'YYYY-MM-DD HH24:MI:SS') AS yelping_since_ts,
            to_date(sr.date, 'YYYY-MM-DD') AS yelping_since_date,
            sr.stars,
            sr.useful,
            sr.funny, 
            sr.cool
        FROM 
        public.staging_review sr 

    """)

    fact_checkin_table_insert = ("""
        INSERT INTO public.fact_checkin(
            business_id, 
            checkin_ts,
            checkin_date,
            year,
            month,
            day,
            hour,
            minute 
        )
        
        SELECT 
            sc.business_id, 
            to_timestamp(sc.date, 'YYYY-MM-DD HH24:MI:SS') AS checkin_ts, 
            to_date(sc.date, 'YYYY-MM-DD') AS checkin_date,
            extract(year from  checkin_ts ) as year,
            extract(month from checkin_ts ) as month,
            extract(day from checkin_ts ) as day,
            extract(hour from checkin_ts ) as hour,
            extract(minute from checkin_ts ) as minute                               
        FROM 
        public.staging_checkin sc 

    """)

    fact_tip_table_insert = ("""
        INSERT INTO public.fact_tip(
            user_id,
            business_id,
            tip_ts,
            tip_date,
            tip_year,
            tip_month,
            tip_day,
            tip_hour,
            tip_minute,
            compliment_count
        )
        
        SELECT 
            user_id,
            business_id,
            to_timestamp(st.date, 'YYYY-MM-DD HH24:MI:SS') AS tip_ts, 
            to_date(st.date, 'YYYY-MM-DD') AS tip_date,
            extract(year from  tip_ts ) as tip_year,
            extract(month from tip_ts ) as tip_month,
            extract(day from tip_ts ) as tip_day,
            extract(hour from tip_ts ) as tip_hour,
            extract(minute from tip_ts ) as tip_minute,
            compliment_count
        FROM 
        public.staging_tip st
        WHERE 
        compliment_count > 0

    """)















    