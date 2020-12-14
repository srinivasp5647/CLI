import mysql.connector
global data_fetch, category_id
global cart_id
mydb = mysql.connector.connect(host='localhost', user='root', password='#', database='shopgarrage',
                               auth_plugin='mysql_native_password')

mycursor = mydb.cursor(buffered=True)

flow = {1: 'user', 2: 'admin'}
print('1 . User',
      ' 2. Admin')
check = int(input('select your behaviour : '))


def take_action(go):
    if go == 1:
        print('hello, ', flow[1])
        user_check()
    else:
        print('hello, ', flow[2])
        admin_function()


def admin_function():
    admin = input('Enter your email : ')
    ad_query = 'SELECT password FROM Admin where email = %s'
    val = (admin,)
    mycursor.execute(ad_query, val)
    admin_data = mycursor.fetchall()
    if admin_data:
        password = input('Enter your password : ')
        if password == admin_data[0][0]:
            print()
            print('*********   Welcome back, Database all yours   **********')
            admin_action()
        else:
            print('Password incorrect')
            admin_function()

    else:
        print('Not a Admin')
        print('1 . User',
              ' 2. Admin')
        check = int(input('select your behaviour : '))
        take_action(check)


def admin_action():
    ad_action = int(input('Add new category dial-1\n For view products dial-2\nSee users activity dial-3\nSee payments dial-4 or dial any key to exit : '))
    print()
    if ad_action == 1:
        cat = input('Enter new category record : ')
        new_category = "INSERT INTO Category(title) VALUES(%s)"
        new_val = (cat,)
        mycursor.execute(new_category, new_val)
        mydb.commit()
        print('New category added successfully')
        admin_action()
    elif ad_action == 2:
        p_query = 'SELECT name, price, description, categoryID FROM Products'
        mycursor.execute(p_query)
        p_details = mycursor.fetchall()
        for p_see in p_details:
            print('*' * 20)
            print(' name : {} \n price : {} \n description : {} \n categotyID : {}'.format(p_see[0],
                                                                                           p_see[1],
                                                                                           p_see[2],
                                                                                           p_see[3]))
        p_ask = input('would like to add new products y/n : ')
        if p_ask == 'y':
            pro = input('Enter new product name : ')
            pri = input('Enter price : ')
            des = input('Enter description : ')
            catid = input('Enter category-id : ')
            new_pro = "INSERT INTO Products(name, price, description, categoryID) VALUES(%s, %s, %s, %s)"
            pro_vals = (pro, pri, des, catid,)
            mycursor.execute(new_pro, pro_vals)
            mydb.commit()
            print('New product added successfully')
            admin_action()
        else:
            admin_action()
    elif ad_action == 3:
        u = 'SELECT cartID, productID, quantity, total FROM Cart_Products'
        mycursor.execute(u)
        all_details = mycursor.fetchall()
        for ad_see in all_details:
            print('*'*20)
            print(' cartID : {} \n productID : {} \n quantity : {} \n total : {}'.format(ad_see[0],
                                                                                         ad_see[1],
                                                                                         ad_see[2],
                                                                                         ad_see[3]))
        cus_ask = input('Would like to check specific user details y/n : ')
        if cus_ask == 'y':
            c_query = 'SELECT * FROM Customers'
            mycursor.execute(c_query)
            c_table = mycursor.fetchall()
            print('----------*****---------( Customer details )------------*****-----------')
            print()
            for each in c_table:
                print('*'*20)
                print('cutomerID : {} \n Name : {} \n Email : {} \n Address : {}'.format(each[0],
                                                                                         each[1],
                                                                                         each[2],
                                                                                         each[3],))
            ad_input = input('Select customer-ID for to view : ')
            cus_cart = 'SELECT cartID FROM Cart WHERE customerID = %s'
            va = (ad_input,)
            mycursor.execute(cus_cart, va)
            cus_cart_id = mycursor.fetchall()
            if cus_cart_id == []:
                print('User not in Cart')
                admin_action()
            else:
                cus_cart_pro = 'SELECT * FROM Cart_Products WHERE cartID = %s'
                cus_v = (cus_cart_id[0][0],)
                mycursor.execute(cus_cart_pro, cus_v)
                cus_cart_details = mycursor.fetchall()
                for cart_pro in cus_cart_details:
                    print('-'*20)
                    print('cpID : {} \n cartID : {} \n productID : {} \n quantity : {} \n total : {}'.format(cart_pro[0],
                                                                                                             cart_pro[1],
                                                                                                             cart_pro[2],
                                                                                                             cart_pro[3],
                                                                                                             cart_pro[4]))
                admin_action()
        else:
            admin_action()

    elif ad_action == 4:
        p = 'SELECT * FROM Payments'
        mycursor.execute(p)
        pay_details = mycursor.fetchall()
        for pays in pay_details:
            print('*'*20)
            print(' paymentID : {} \n cartID : {} \n amount : {} \n discount : {} \n total : {} \n Paid : {}'.format(pays[0],
                                                                                                                     pays[1],
                                                                                                                     pays[2],
                                                                                                                     pays[3],
                                                                                                                     pays[4],
                                                                                                                     pays[5]))
        admin_action()

    else:
        print('----------(  THANK YOU FOR SPENDING TIME IN DATABASE  )---------------')
        exit()


def user_check():
    global data_fetch
    user = input('enter your registerd email : ')
    action = 'SELECT customerID, name FROM Customers WHERE email = %s'
    val = (user,)
    mycursor.execute(action, val)
    data_fetch = mycursor.fetchall()
    if data_fetch:
        print()
        print(' *****   welcome back, {}  *****'.format(data_fetch[0][1]))
        print()
        print('---------- Njoy your shopping :-) ------------')
        print()
        user_category()
    else:
        print()
        n_action = input('Sorry your email is not registerd, would you like to register y/n : ')
        if n_action == 'y':
            name = input('enter your name : ')
            address = input('enter your address : ')
            dat = 'INSERT INTO Customers(name, email, address) VALUES(%s, %s, %s)'
            vals = (name, user, address)
            mycursor.execute(dat, vals)
            mydb.commit()
            user_category()
        else:
            again = input('would you like try again y/n : ')
            if again == 'y':
                user_check()
            else:
                print('have a nice day !!')
                exit()


def user_category():
    global category_id
    cat = 'SELECT * FROM Category'
    mycursor.execute(cat)
    cat_data = mycursor.fetchall()

    print('categories are...')
    categories = []
    for c in cat_data:
        print(str(c[0]) + '.' + c[1], end='\n')
        categories.append(c[0])

    cart_ask = input('would you like to check your cart y/n : ')
    if cart_ask == 'y':
        checking_user = 'SELECT cartID FROM Cart WHERE customerID = %s'
        vals = (data_fetch[0][0],)
        mycursor.execute(checking_user, vals)
        cart_id = mycursor.fetchall()
        if cart_id == []:
            print('No items in your cart')
            user_category()
        else:
            cart_view(cart_id)
    else:
        pass
    print()
    selection = int(input('Choose your category number for shopping : '))
    print()
    if selection in categories:
        cat_id = 'SELECT categoryID FROM Category WHERE categoryID = %s'
        val = (selection,)
        mycursor.execute(cat_id, val)
        id = mycursor.fetchall()
        category_id = 0
        for i in id:
            category_id = i[0]
        user_products(category_id)


def user_products(category_id):
    global cart_id
    pro = 'SELECT productID, name FROM Products where categoryID = %s'
    pro_val = (category_id,)
    mycursor.execute(pro, pro_val)
    products = mycursor.fetchall()
    print()
    print('------ products --------')
    for pros in products:
        print(pros[1])
    print()
    choosing = input('select your product to view details : ')
    pro_details = 'SELECT productID, price, description FROM Products WHERE name = %s'
    val = (choosing,)
    mycursor.execute(pro_details, val)
    details = mycursor.fetchall()
    print()

    for de in details[0]:
        print(de)
    print()
    buy = input('Would you like to add this product to cart y/n : ')

    if buy == 'y':
        cart_customer = 'SELECT cartID FROM Cart WHERE customerID = %s LIMIT 1'
        values = (data_fetch[0][0],)
        # print(data_fetch[0][0])
        mycursor.execute(cart_customer, values)
        cart_id = mycursor.fetchall()
        # print(cart_id)
        if cart_id:
            print("Adding Your Products into Cart")
            pro_check = "SELECT productID FROM Cart_Products WHERE cartID = %s"
            pro_val = (cart_id[0][0],)
            mycursor.execute(pro_check, pro_val)
            pro_id = mycursor.fetchall()
            if details[0][0] in list(map(lambda x: x[0], pro_id)):
                update_quantity = 'UPDATE Cart_Products SET quantity=quantity+1, total=total+total WHERE productID = %s'
                up_val = (details[0][0],)
                mycursor.execute(update_quantity, up_val)
                mydb.commit()
                print('Added to cart successfully !!')
                final_asking = int(
                    input('want to change Category dial-1\ngo to products dial-2\ngo to your cart dial-3 : '))
                if final_asking == 1:
                    user_category()
                elif final_asking == 2:
                    user_products(category_id)
                elif final_asking == 3:
                    cart_view(cart_id)
            else:
                cart_product = 'INSERT INTO Cart_Products(cartID, productID, quantity, total) values(%s, %s, %s, %s)'
                val = (cart_id[0][0], products[0][0], 1, details[0][1],)
                mycursor.execute(cart_product, val)
                mydb.commit()
                print('Added to cart successfully')
                print()
                final_asking = int(input('want to change Category dial-1\ngo to products dial-2\ngo to your cart dial-3 : '))
                if final_asking == 1:
                    user_category()
                elif final_asking == 2:
                    user_products(category_id)
                elif final_asking == 3:
                    cart_view(cart_id)
        elif cart_id == []:
            print("Please be paitnet Your Cart is Creating...... ")
            cus_cart = 'INSERT INTO Cart(customerID) values(%s)'
            vals = (data_fetch[0][0],)
            mycursor.execute(cus_cart, vals)
            mydb.commit()
            cart_customer = 'SELECT cartID FROM Cart WHERE customerID = %s LIMIT 1'
            values = (data_fetch[0][0],)
            mycursor.execute(cart_customer, values)
            cart_id = mycursor.fetchall()
            cart_product = 'INSERT INTO Cart_Products(cartID, productID, quantity, total) values(%s, %s, %s, %s)'
            val = (cart_id[0][0], products[0][0], 1, details[0][1],)
            mycursor.execute(cart_product, val)
            mydb.commit()
            print('Added to cart successfully')
            print()
            final_asking = int(
                    input('want to change Category dial-1\ngo to products dial-2\ngo to your cart dial-3 : '))
            if final_asking == 1:
                user_category()
            elif final_asking == 2:
                user_products(category_id)
            elif final_asking == 3:
                cart_view(cart_id)
    else:
        print()
        ask = input('want to change category y/n or dial any key to exit : ')
        if ask == 'y':
            user_category()
        elif ask == 'n':
            user_products(category_id)
        else:
            print("------- THANKS FOR SHOPPING --------")
            exit()

def cart_view(cart_id):
    cart_products = []
    print('this is your cart')
    print()
    cart_query = 'SELECT productID, quantity, total FROM Cart_Products WHERE cartID = %s AND paid = 0'
    val = (cart_id[0][0],)
    mycursor.execute(cart_query, val)
    cart_details = mycursor.fetchall()
    print('cart-details : ', cart_details)
    if cart_details == []:
        print('You don"t have any items in cart')

    else:

        for products in cart_details:
            product_query = 'SELECT name, price FROM Products WHERE productID = %s'
            vals = (products[0],)
            mycursor.execute(product_query, vals)
            product = mycursor.fetchall()

            cart_products.append({
                "product_name": product[0][0],
                "product_quantity": products[1],
                "product_actual_price": product[0][1],
                "sub_total": products[1] * product[0][1]
            })

        for added_product in cart_products:
            print("*"*20)
            print(" Name: {} \n Quantity: {} \n Price: {} \n Sub Total: {}".format(added_product["product_name"],
                                                                                   added_product["product_quantity"],
                                                                                   added_product["product_actual_price"],
                                                                                   added_product["sub_total"]
                                                                                   )
                  )

        cart_remove = input('Want to remove any item from your cart y/n : ')
        print(cart_remove)
        print(cart_remove == 'y')
        if cart_remove == 'y':
            remove_item = input('select your product name to delete : ')
            for item_name in cart_products:
                if remove_item in item_name['product_name']:
                    item_query = 'SELECT productID FROM Products WHERE name = %s'
                    it_val = (remove_item,)
                    mycursor.execute(item_query, it_val)
                    remove_id = mycursor.fetchall()
                    check_cart = 'SELECT quantity FROM Cart_Products WHERE productID = %s AND cartID = %s'
                    cart_val = (remove_id[0][0], cart_id[0][0])
                    mycursor.execute(check_cart, cart_val)
                    quantity_value = mycursor.fetchall()
                    if quantity_value[0][0] > 1:
                        quantity_update = 'UPDATE Cart_Products SET quantity=quantity-1, total=total-total WHERE productID= %s AND cartID= %s'
                        q_val = (remove_id[0][0], cart_id[0][0])
                        mycursor.execute(quantity_update, q_val)
                        mydb.commit()
                        cart_view(cart_id)
                    else:
                        quantity_update = 'DELETE FROM Cart_Products WHERE productID= %s AND cartID= %s'
                        q_val = (remove_id[0][0], cart_id[0][0])
                        mycursor.execute(quantity_update, q_val)
                        mydb.commit()
                        cart_view(cart_id)
        else:
            print('yooooooooo')
            pass
        print()
        question = int(input('Continue Shopping dial-1\nGo to payment dial-2 : '))
        if question == 1:
            user_category()
        elif question == 2:
            pay_auery = 'SELECT cartId FROM Cart WHERE customerID = %s'
            pay_val = (data_fetch[0][0],)
            mycursor.execute(pay_auery, pay_val)
            pay_cus_id = mycursor.fetchall()
            final_order = []
            final_pro = 'SELECT productID, quantity, total FROM Cart_Products WHERE cartID = %s AND paid = 0'
            f_val = (pay_cus_id[0][0],)
            mycursor.execute(final_pro, f_val)
            f_details = mycursor.fetchall()
            for f in f_details:
                pay_pro = 'SELECT name, price FROM Products WHERE productID = %s'
                v = (f[0],)
                mycursor.execute(pay_pro, v)
                p = mycursor.fetchall()

                final_order.append({
                    "product_name": p[0][0],
                    "product_quantity": f[1],
                    "product_actual_price": p[0][1],
                    "sub_total": f[1] * p[0][1],
                    })

            for payment in final_order:
                print('*'*20)
                print(' Name : {} \n Price : {} \n Quantity : {} \n Total : {}'.format(payment['product_name'],
                                                                                       payment['product_actual_price'],
                                                                                       payment['product_quantity'],
                                                                                       payment['sub_total']))

            final_transaction_total = 0
            for i in final_order:
                final_transaction_total += i["sub_total"]
            transaction(pay_cus_id, f_details, final_transaction_total)


def transaction(pay_cus_id, f_details, final_transaction_total):
    if final_transaction_total > 10000:
        print('You will get a discount of 500 and your total bill is : ' + str(final_transaction_total - 500))
    else:
        print('You will get a discount of 500 and your total bill is : ' + str(final_transaction_total))
    pay_money = float(input('Enter your payment amount : '))
    discount = 500 if (final_transaction_total > 10000) else 0
    if pay_money == (final_transaction_total - discount):
        print('payment successfull')
        update_paid = "UPDATE Cart_Products SET paid = 1 WHERE cartID = %s"
        up_vals = (pay_cus_id[0][0],)
        mycursor.execute(update_paid, up_vals)
        mydb.commit()
        up_pay = 'INSERT INTO Payments(cartID, amount, discount, total, paid) VALUES(%s, %s, %s, %s, %s)'
        u_val = (pay_cus_id[0][0], final_transaction_total, discount, final_transaction_total - discount, 1)
        mycursor.execute(up_pay, u_val)
        mydb.commit()
        user_category()
    else:
        print('Please enter valid amount')
        transaction(pay_cus_id, f_details, final_transaction_total)


if __name__ == '__main__':
    take_action(check)
