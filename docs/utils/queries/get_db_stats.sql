SELECT (SELECT COUNT(*) FROM "Images")                                                                              AS images_count,
       (SELECT COUNT(*) FROM "Images" WHERE "Images".nsfw = 'questionable')                                         AS images_nsfw__questionable__count,
       (SELECT COUNT(*) FROM "Images" WHERE "Images".nsfw = 'nsfw')                                                 AS images_nsfw__nsfw__count,
       (SELECT COUNT(*) FROM "Images" WHERE "Images".original = true)                                               AS images_original__true__count,
       (SELECT COUNT(*) FROM "Images" WHERE "Images".original = false)                                              AS images_original__false__count,
       (SELECT COUNT(*)
        FROM "Images"
        WHERE ("Images".height >= 2160 AND "Images".width >= 3840)
           OR ("Images".height >= 3840 AND "Images".width >= 2160))                                                 AS images_resolution__uhd__count,
       (SELECT COUNT(*)
        FROM "Images"
        WHERE (("Images".height >= 1080 AND "Images".width >= 1920) OR
               ("Images".height >= 1920 AND "Images".width >= 1080))
          AND (("Images".height < 2160 AND "Images".width < 3840) OR
               ("Images".height < 3840 AND "Images".width < 2160)))                                                 AS images_resolution__fhd__count,
       (SELECT COUNT(*)
        FROM "Images"
        WHERE (("Images".height >= 1280 AND "Images".width >= 720) OR
               ("Images".height >= 720 AND "Images".width >= 1280))
          AND (("Images".height < 1080 AND "Images".width < 1920) OR
               ("Images".height < 1920 AND "Images".width < 1080)))                                                 AS images_resolution__hd__count,
       (SELECT COUNT(*)
        FROM "Images"
        WHERE (("Images".height >= 480 AND "Images".width >= 640) OR ("Images".height >= 640 AND "Images".width >= 480))
          AND (("Images".height < 720 AND "Images".width < 1280) OR
               ("Images".height < 1280 AND "Images".width < 720)))                                                  AS images_resolution__sd__count,
       (SELECT COUNT(*)
        FROM "Images"
        WHERE "Images".height > "Images".width)                                                                     AS images_orientation__portrait__count,
       (SELECT COUNT(*)
        FROM "Images"
        WHERE "Images".height < "Images".width)                                                                     AS images_orientation__landscape__count,
       (SELECT COUNT(*) FROM "Categories")                                                                          AS categories_count,
       (SELECT COUNT(*)
        FROM "Categories"
        WHERE "Categories".type = 'setting')                                                                        AS categories_type__setting__count,
       (SELECT COUNT(*)
        FROM "Categories"
        WHERE "Categories".type = 'character')                                                                      AS categories_type__character__count,
       (SELECT COUNT(*) FROM "Categories" WHERE "Categories".type = 'format')                                       AS categories_type__format__count,
       (SELECT COUNT(*) FROM "Categories" WHERE "Categories".nsfw = true)                                           AS categories_nsfw__nsfw__count,
       (SELECT COUNT(*) FROM "Artists")                                                                             AS artists_count,
       (SELECT COUNT(*) FROM "Characters")                                                                          AS characters_count,
       (SELECT COUNT(*)
        FROM (SELECT DISTINCT "Characters".source
              FROM "Characters"
              WHERE "Characters".source IS NOT NULL) AS temp)                                                       AS characters_sources__unique__count