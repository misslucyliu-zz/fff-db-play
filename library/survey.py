from collections import defaultdict


def return_actives(push_con):
    """Return active customers"""
    # get actives and active selects
    push_cur = push_con.cursor()
    push_cur.execute("""SELECT users.account_code,user_woo_users.woo_user_id,
                        recurly_subscriptions.state,users.selectmanual FROM recurly_subscriptions
                        LEFT JOIN users ON users.account_code = recurly_subscriptions.account_code
                        LEFT JOIN user_woo_users ON user_woo_users.user_id = users.id
                        WHERE recurly_subscriptions.state = 'active' AND users.account_code != ''
                        AND recurly_subscriptions.account_code != ''""")
    actives_query = push_cur.fetchall()

    # create actives and active selects dictionaries
    actives = {}
    active_select = {}
    for row in actives_query:
        actives[row[1]]={'select':row[3],'state':row[2]}
        if row[3] == 1:
            active_select[row[1]]={'select':row[3],'state':row[2]}

    return actives


def return_skin_tone_dict(prod_con,actives):
    """Results of skin tone survey and skin tone in personal survey"""
    # get skin tone survey results
    prod_cur = prod_con.cursor()
    prod_cur.execute("""SELECT shop_rg_lead.created_by,shop_rg_lead_detail.value,MAX(shop_rg_lead.id)
                        FROM shop_rg_lead_detail 
                        JOIN shop_rg_lead ON shop_rg_lead.id = shop_rg_lead_detail.lead_id
                        WHERE ((shop_rg_lead_detail.form_id = 8 AND shop_rg_lead_detail.field_number = 1)
                        OR (shop_rg_lead_detail.form_id = 6 AND shop_rg_lead_detail.field_number = 8))
                        AND shop_rg_lead.created_by is not null
                        GROUP BY shop_rg_lead.created_by""")
    skin_tone_query = prod_cur.fetchall()

    # create skin tone survey dictionary
    skin_tone_dict = {}
    for row in skin_tone_query:
        if row[0] in actives:
            skin_tone_dict[row[0]] = row[1]

    return skin_tone_dict


def return_spring_select_dict(prod_con,actives):
    """Return Spring 2016 Select survey results"""
    # get spring select survey results
    prod_cur = prod_con.cursor()
    prod_cur.execute("""SELECT shop_rg_lead.created_by, shop_rg_lead_detail.value, MAX(shop_rg_lead.id)
                        FROM shop_rg_lead_detail 
                        JOIN shop_rg_lead ON shop_rg_lead.id = shop_rg_lead_detail.lead_id
                        WHERE shop_rg_lead_detail.form_id = 7 AND shop_rg_lead_detail.field_number =9
                        AND shop_rg_lead.created_by is not null
                        GROUP BY shop_rg_lead.created_by""")

    spring_select_query = prod_cur.fetchall()

    # create spring survey dictionary
    spring_select_dict = {}
    for row in spring_select_query:
        if row[0] in actives:
            spring_select_dict[row[0]] = row[1]

    return spring_select_dict


def return_skus(sku_key, actives, skin_tone_dict, spring_select_dict):
    """Spring 2016 SKU counts based on survey results"""
    skus = defaultdict(int)
    for active in actives:
        skin_tone = None
        select = None
        if active in skin_tone_dict:
            skin_tone = int(skin_tone_dict[active])
            if skin_tone < 4:
                skin_tone = 0
            else:
                skin_tone = 1
        if active in spring_select_dict:
            select = spring_select_dict[active]
            if select == 'Surprise Me!':
                select = None
        sku = (skin_tone,select)
        if sku in sku_key:
            skus[sku_key[sku]] += 1
    return skus


sku_key = {(0,None):'Q-1601A-G1',
    (1,None):'Q-1601A-G2',
    (0,'Dream'):'Q-1601A-1A',
    (0,'Happy'):'Q-1601A-1B',
    (0,'Inspire'):'Q-1601A-1C',
    (0,'Love'):'Q-1601A-1D',
    (1,'Dream'):'Q-1601A-2A',
    (1,'Happy'):'Q-1601A-2B',
    (1,'Inspire'):'Q-1601A-2C',
    (1,'Love'):'Q-1601A-2D'}
    

sku_order = ['Q-1601A-G1','Q-1601A-G2',
             'Q-1601A-1A','Q-1601A-1B','Q-1601A-1C','Q-1601A-1D',
             'Q-1601A-2A','Q-1601A-2B','Q-1601A-2C','Q-1601A-2D']