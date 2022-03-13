CREATE FUNCTION public.assign_neighbourhood_id()
    RETURNS TRIGGER
    LANGUAGE 'plpgsql'
    
AS $BODY$
    DECLARE
        rec record;
    BEGIN 
        SELECT n.id INTO rec FROM public.neighbourhoods as n 
        WHERE ST_Contains(n.geom, NEW.geom);
        
        IF NOT FOUND THEN
            RETURN OLD;
		ELSE
			NEW.neighbourhood_id = rec.id;
			RETURN NEW;
        END IF;
    END 
$BODY$;