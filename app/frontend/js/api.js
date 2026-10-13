const API_BASE="/api/v1";
async function apiRequest(path, options={}) {
  const headers={"Content-Type":"application/json",...(options.headers||{})};
  const token=localStorage.getItem("access_token");
  if(token) headers.Authorization=`Bearer ${token}`;
  const response=await fetch(API_BASE+path,{...options,headers});
  const data=await response.json().catch(()=>({}));
  if(!response.ok) throw new Error(data.detail||`Request failed (${response.status})`);
  return data;
}
function getCart(){try{return JSON.parse(localStorage.getItem("cart")||"[]")}catch{return []}}
function saveCart(cart){localStorage.setItem("cart",JSON.stringify(cart));updateCartCount()}
function updateCartCount(){const node=document.querySelector("#cart-count");if(node)node.textContent=getCart().reduce((sum,item)=>sum+item.quantity,0)}
function money(value){return new Intl.NumberFormat("en-IN",{style:"currency",currency:"INR"}).format(Number(value))}
document.addEventListener("DOMContentLoaded",updateCartCount);
