//import blockchain.BlockChain;
//import com.google.gson.stream.JsonWriter;
import blockchain.BCJsonUtils;
import blockchain.BlockChain;
import blockchain.Transactions;
import blockchain.Block;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.io.FileWriter;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.io.FileReader;
import java.io.Reader;

public class Main {
    /**

     Crée une blockchain = registre publique de transactions monétaires signés 
     * Focus sur le création monétaire
     */

    public static void main(String[] args) throws FileNotFoundException {

        int Index = 1; // hauteur des blocs
        int maxBlock = 1000; // ça suffira pour tester
        int maxUsers = 10; // c'est peu mais le Bitcoin a commencé comme ça
        int feeRate = 5; //poucentage pour les frais
        int difficulty = 4;
        long reward = 50L*100000000L;// en satoBnb
        long satoBnb = 100000000L; // 10^8
        int inflationRounds = 0; // tient compte du genesis
        int limit = 20;// nb tx entre deux divisions de la récompence
        int nbTxBlock = 5; // nb max de tx par bloc
        ArrayList<Transactions> globalTxFIFO = new ArrayList<>(); // FIFO globale de tx 
        int flag = 0;
        
        System.out.println("Difficulty = "+difficulty);
        System.out.println("Initial reward in satoBnb = "+reward);
        System.out.println("------------ Genesis from que dalle -----------");
        BlockChain BlockC = new BlockChain(difficulty,reward); // doit être publique
        
        System.out.println("Money supply 0 = "+BlockC.moneySupply); // debug
        // phase d'inflation
        // 1 - création de monnaie : helicopter money, openbar, c'est coinBase qui régale
        System.out.println("--------- Helicopter money -----------");
        for (int count = 0 ; count < maxUsers ; count++){
//            System.out.print("===> utxo list :");
//            BlockC.printUtxoList();// debug
            Block lb = BlockC.getLastBlock();
            String previousHash = lb.getBlockHash();
            //lb.printBlock();
            BlockC.addBlock(BlockC.helicopterMoney("User"+count,Index,previousHash,reward));
            if ((Index+1) % limit == 0) {
                reward /=2;
                inflationRounds++;
                System.out.println("Money supply 1 = "+BlockC.moneySupply);
            }
            Index=Index+1;  
            //System.out.println("Money supply H = "+BlockC.moneySupply); // debug
        }
        
        // 2 - le marché et sa loi impitoyable avec inflation puis sans
        System.out.println("-------------- Bourse : la main invisible du marché vs le poing de la vengeance prolétaire --------------");
 
        for (int count = 1 ; count <=maxBlock ; count++){
            // ajout d'un nombre aléatoire de tx
            //System.out.print("===> utxo list :");BlockC.printUtxoList();// debug
            int nbTx = ThreadLocalRandom.current().nextInt(1, 1 + 1); // au pif ! Une seule pour mise au point
            //System.out.println("nbTx = "+nbTx); // debug
            for (int i=1;i<=nbTx;i++){ // choix aléatoire de Alice et Bob
                int numUser1 = ThreadLocalRandom.current().nextInt(0, maxUsers); // Alice
                int numUser2 = ThreadLocalRandom.current().nextInt(0, maxUsers); // Bob
                long amount = (long) ThreadLocalRandom.current().nextInt(1, 10 + 1); // montant au pif en Bnb
                amount = amount*satoBnb; // on convertit en satoBnb
                Transactions tx = new Transactions("market"); // génération de la tx Alice --> Bob
                BlockC.utxoList = tx.marketTx(BlockC.utxoList, "User"+numUser1, "User"+numUser2, amount, feeRate); // tx selon le mode général
                //System.out.println("===> Tx market : amount :"+amount+" Alice : User"+numUser1+" Bob : User"+numUser2); // debug
                //System.out.println("-------------------"); // debug
                globalTxFIFO.add(tx); // mise en file pour le minage
            }
            // choose miner
            int pickMiner = ThreadLocalRandom.current().nextInt(1, 10 + 1);
            String minerName = "User"+pickMiner;
            Block newBlk = BlockC.makeBlock(Index, globalTxFIFO,reward,minerName);

             // il faut que les tx de newBlk soient retirées de global
            for (int i = 0 ; i<newBlk.getTransaction().size();i++){
                globalTxFIFO.remove(newBlk.getTransaction().get(i));
            }
            // doit-on continuer l'inflation ?
            BlockC.addBlock(newBlk);
            if ((Index + 1) % limit==0 && reward > 0) {
                reward /=2;
                System.out.print("Reward = "+reward);
                inflationRounds++;
                System.out.println(" Money supply 2 = "+BlockC.moneySupply+"("+(float) BlockC.moneySupply/satoBnb+" Bnb)");
            }
            // doit-on diviser la récompence ?
            if (reward <= 0){
                reward = 0;
                if (flag == 0) {
                    System.out.println("---------------- Fin de la phase d'inflation -----------------");
                    System.out.println("Money supply = "+BlockC.moneySupply+"("+(float) BlockC.moneySupply/satoBnb+" Bnb)");
                    System.out.println("Inflation rounds = "+inflationRounds);
                    flag = 1;
                }
            }
            Index=Index+1;
            
        }

        System.out.println("-------------------- Dump de la blockchain ----------------------");
        for (int i=0;i<BlockC.BC.size();i++){
            BlockC.BC.get(i).printBlock();
        }

        // on sauve en JSON
        BCJsonUtils.BCJsonWriter(BlockC, "registre.json");
        
//        // On lit pour vérifier
//        BlockChain BlockC3 = BCJsonUtils.BCJsonReader("registre.json");
//        System.out.println("----------------------- Blockchain lue depuis JSON --------------------");
//        for (int i=0;i<BlockC3.BC.size();i++){
//            BlockC.BC.get(i).printBlock();
//        }
        // liste utxo
//        System.out.println("UTXO List :");
//        for (int i=0;i<BlockC.utxoList.size();i++){
//            BlockC.utxoList.get(i).print();
//        }
    }
}


