package blockchain;

//

/*
 doc
 */

//package blockchain;


/**
 *
 * @author vincent
 */
import blockchain.Transactions;
//import blockchain.TxInputs;
import java.util.List;
import java.util.*;
import java.util.Arrays;
import java.util.ArrayList;
import java.io.FileReader;
import java.io.Reader;

//import com.google.gson.Gson;
import java.io.IOException;
import java.util.concurrent.ThreadLocalRandom;
/**
 *
 * @author vincent
 */
public class BlockChain {
    public int difficulty;
    public int nbBlocks;
    public List<Block> BC = new ArrayList<>();
    public ArrayList<TxOutputs> utxoList;
    public long moneySupply; // masse monétaire
    
    public BlockChain(int difficulty,long reward){
        this.nbBlocks = 1;
        this.difficulty = difficulty;
        this.utxoList = new ArrayList<>();
        this.moneySupply = 0L;
        this.BC.add(0,this.createGenesisBlock(reward));// liste vide avant
    }
    
    public long updateMoneySupply(long amount){
        this.moneySupply += amount;
        return this.moneySupply;
}
    
    public void printUtxoList(){
        for (int i=0;i<this.utxoList.size();i++){
            System.out.println(this.utxoList.get(i).lockingScript+"Amount : "+this.utxoList.get(i).amount);
        }
    }
    
    public Block createGenesisBlock(long reward){
        ArrayList<Transactions> genesisTransactions = new ArrayList<>();
        Transactions tx = new Transactions("genesis");
        tx.coinbaseTx(reward, "Creator");
        this.updateMoneySupply(reward);
        genesisTransactions.add(0,tx);
        Block nb = new Block(0,"0", genesisTransactions,"Creator");
        utxoList.add(tx.lstOutputs.get(0)); // liste globale
        nb.mineBlock(difficulty,"Creator");
        return nb;
    }
    
    public Block helicopterMoney(String user,int index,String previousHash,long reward){
        ArrayList<Transactions> heliTransactions = new ArrayList<>();
        Transactions tx = new Transactions("helicopter");
        tx.coinbaseTx(reward, user);
        heliTransactions.add(0,tx);
        utxoList.add(tx.lstOutputs.get(0)); // liste globale
        //this.utxoList.add(tx); 
        Block nb = new Block(index,previousHash, heliTransactions,user);
        nb.mineBlock(difficulty,user);
        this.updateMoneySupply(reward);
        return nb;
    }
    
    public int getDifficulty(){
        return difficulty;
    }
    
    public List<Block> getBlockList(){
        return BC;
    }
    
    public int getBlockNb(){
        return nbBlocks;
    }
    
    public Block getLastBlock(){
        //int lon = this.BC.size()-1;
        //return this.BC.get(lon);
        return this.BC.get(0);
    }   
    
    public Block makeBlock(int index,ArrayList<Transactions> txList,long reward,String minerName){
        // c'est le mineur qui fait et ajoute le bloc
        ArrayList<Transactions> blockTransactions = new ArrayList<>(); // liste de tx pour le bloc
        ArrayList<Transactions> lstTransactionsFees = new ArrayList<>(); // liste de tx
        //int nbTx = 2; // une tx à la fois
        int nbTx = ThreadLocalRandom.current().nextInt(2, 4 + 1); // au pif ! entre 1 et 4
        for (int i = 1;i <= Math.min(nbTx,txList.size());i++){ // pour chaque tx et au cas où rien
            blockTransactions.add(0,txList.get(0)); // 1ere tx -> dans la liste
            txList.remove(0); // sur copie locale
        }
        //System.out.println("====> "+nbTx+" "+blockTransactions.size());// debug
        // on commence à construire le bloc
        String previousHash = this.getLastBlock().getBlockHash();
        // récompense
        if (reward > 0){
            Transactions tx = new Transactions("coinBase");
            //System.out.println("make bloc");tx.printTrans();
            if (tx.nbOutputs != 0){
                utxoList.add(tx.lstOutputs.get(0)); // liste globale
                //System.out.println("Vérification tx coinbase");
                //tx.lstOutputs.get(0).print();
            }
            
            tx.coinbaseTx(reward, minerName);
            for (int i=0;i<blockTransactions.size();i++){
                //System.out.println("===> boucle "+i+" "+blockTransactions.size());//debug
                Transactions txI = blockTransactions.get(i);
                long fees = txI.fees();
                Transactions txFees = new Transactions("fees");
                txFees.lstInputs = txI.lstInputs; // c'est le même qui paye
                ArrayList<String> lockScript = new ArrayList<>();
                lockScript = txI.lockScript(minerName);
                if (lockScript.isEmpty())
                    System.out.println("PB makeBlock");
                TxOutputs outTx = new TxOutputs(0,"0",lockScript,fees);
                outTx.hash = outTx.calculateHash();
                txFees.lstOutputs.add(outTx);
                txFees.nbInputs = txFees.lstInputs.size();
                txFees.nbOutputs = txFees.lstOutputs.size();
                utxoList.add(txFees.lstOutputs.get(0));
                lstTransactionsFees.add(0,txFees);// ajout des frais
            }
            blockTransactions.addAll(lstTransactionsFees);
            blockTransactions.add(0,tx);// le mineur se paye
            this.updateMoneySupply(reward);
        }
        
        //System.out.println("XXX2XX====> "+nbTx+" "+blockTransactions);
        Block nb = new Block(index,previousHash, blockTransactions,minerName);
        nb.mineBlock(difficulty,minerName);// ce doit être miné avant
        return nb;
    }
    
    public void addBlock(Block blk){
        // déjà miné
        this.BC.add(0,blk);
        (this.nbBlocks)++;
    }
    
    public boolean isBlockChainValid(List blockChain) {
        if (blockChain.size() > 1) {
            for (int i = blockChain.size()-1; i >1 ; i--) {
                Block currentBlock = (Block) blockChain.get(i);
                Block nextBlock = (Block) blockChain.get(i-1);
                if (!(currentBlock.calculateHash().equals(currentBlock.blockHash)))
                    return false;
                if (!(nextBlock.getPreviousHash().equals(currentBlock.getBlockHash()))) {
                    return false;
                }
            }
        }
        return true;
    }
        
}


