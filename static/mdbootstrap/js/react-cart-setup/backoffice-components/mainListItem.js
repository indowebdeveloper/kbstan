
return (
    <tr data-product-id='{item.product.id}'>
        <td>
            {item.product.id}
        </td>
        <td>
            {item.product.name}
        </td>
        <td>
            <div class='input-group'>
                <div class='input-group-append bg-primary p-0 rounded-left' style='margin-right: -3px;'>
                    <button class='btn btn-sm btn-primary rounded-left font-weight-bold m-0 px-2 py-1' data-user-id='{user.id}' data-target-field='#fieldFor{item.product.id}' data-id='{item.product.id}' data-action='remove' onclick='sendRequest(alter_cart_endpoint, this)' >-1</button>
                </div>
                <input readonly type='text' id='fieldFor{item.product.id}' value="{item.quantity}" class='user-selectable-none py-1 text-center' style='width:50px'>
                </p>
                <div class='input-group-append bg-primary p-0 rounded-right'  style='margin-left: -3px;'>
                    <button class='btn btn-sm btn-primary font-weight-bold px-2 py-1 m-0 rounded-right' data-user-id='{user.id}' data-target-field='#fieldFor{item.product.id}' data-id='{item.product.id}' data-action='add' onclick='sendRequest(alter_cart_endpoint, this)' >+1</button>
                </div>
                <button data-user-id='{user.id}' data-target-field='#fieldFor{item.product.id}' data-id='{item.product.id}' data-action='delete' onclick='sendRequest(alter_cart_endpoint, this)' class='btn btn-sm btn-danger px-3 py-2 m-0 ml-3 clickable clickable-large'>
                    <i class="fas fa-trash-alt text-white"></i>
                </button>
            </div>
        </td>
        <td>
            {item.product.sku}
        </td>
        <td>
            {item.product.bottomPrice}
        </td>
        <td>
            {item.product.price}
        </td>
        <td>
            FULL PRICE?! {item.product.price}
        </td>
    </tr>
);