package blockchain;

import static java.lang.System.in;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.LinkedList;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author vincent
 */
public class TxOutputs {
    public int outIndex; // numéro de tx ; zéro si coinbase
    public String hash; // à virer
    public ArrayList<String> lockingScript; // "" si coinbase 
    public long amount; // in satoBnb
    
    public TxOutputs(int index,String hash,ArrayList<String> lockingScript,long amount) {
        this.outIndex = index;
        this.hash = hash; // à virer
        this.lockingScript = lockingScript;
        this.amount = amount;
    }
    
    public void print(){
        //System.out.println("--- Output List ---");
        System.out.print("out index : "+this.outIndex);
        //System.out.print(" ; hash : "+this.hash);
        System.out.print(" ; lock : "+this.lockingScript);
        System.out.println(" ; Amount : "+this.amount);
    }
    
    public String calculateHash() { // à virer
        String calculatedhash = HashUtil.applySha256(String.valueOf(outIndex)+lockingScript+amount);
        return calculatedhash;
    }
    
    public boolean verify(ArrayList<String> unlockScript){
        // faire fonctionner une pile avec lock.unlock
        ArrayList<String> script = (ArrayList<String>) this.lockingScript.clone();
        ArrayList<String> operators = new ArrayList<>( Arrays.asList("DUP", "HASH", "EQ", "VER") );
        //System.out.println("==> verify : locking script (Tx) : "+script);// debug
        //System.out.println("==> verify : Unlock script (Tx) : "+unlockScript);// debug
        script.addAll(unlockScript); 
        //System.out.println("==> verify : script (Tx) : "+script);// debug
        Deque<String> pile = new LinkedList<>();
        for (String item : script) {
            //System.out.println("==> item : "+item);// debug
            //System.out.println("===> PILE = "+pile); // debug
            if (!operators.contains(item)) 
                pile.push(item);
            else {
                //System.out.println("ELSE"); // debug
                if ("DUP".equals(item)){
                    String top = pile.peek();
                    pile.push(top);
                }
                if ("HASH".equals(item)){
                    String top = pile.pop();
                    pile.push("H("+top+")");
                }
                if ("EQ".equals(item)){
                    String top1 = pile.pop();
                    String top2 = pile.pop();
                    //System.out.println("EQ : top1 : |"+top1+"| top2 : |"+top2+"|");// debug
                    if (!top1.equals(top2)){
                        //System.out.println("==> verify : NON EQ");
                        return false;
                    }
                }
                if ("VER".equals(item)){
                    String top1 = pile.pop();
                    String top2 = pile.pop();
                    String user1 = top1.substring(8,top1.length()-1);
                    String user2 = top2.substring(9,top2.length()-1);
                    //System.out.println("VER : "+top1+" : "+top2);
                    //System.out.println("VER : user1 : |"+user1+"| ; user2 : |"+user2+"|");// debug
                    // demande au wallet de chiffrer la tx avec sa clef privée et vérifie avec la clef publique
                    if (!user1.equals(user2)){
                        //System.out.println("==> verify : NON VER");
                        return false;
                    }
                    else return true;
                }
            }
        }
        return true;
    }
}
