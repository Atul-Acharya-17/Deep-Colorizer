from tqdm.auto import tqdm
import torch

def train_pix2pix(gen, disc, dataloader, gen_opt, disc_opt, gan_loss_fn, l1_loss_fn, device, epochs=5, penalty=100.):
    gen_loss_list = []
    disc_loss_list = []

    for epoch in range(epochs):

        for data in tqdm(dataloader):

            #Move grey and color to cuda
            
            L = data['L'].to(device)
            ab = data['ab'].to(device)

            # Update Disciminator

            disc_opt.zero_grad()
            fakes = gen(L).detach()
            fake_pred = disc(L, fakes)
            real_pred = disc(L, ab)
            fake_loss = gan_loss_fn(fake_pred, torch.zeros_like(fake_pred))
            real_loss = gan_loss_fn(real_pred, torch.ones_like(real_pred))
            disc_loss = 0.5 * (fake_loss + real_loss)
            disc_loss.backward()
            disc_opt.step()

            # Update Generator

            gen_opt.zero_grad()
            gen_color = gen(L)
            disc_pred = disc(L, gen_color)
            loss = gan_loss_fn(disc_pred, torch.ones_like(disc_pred))
            l1_loss = l1_loss_fn(ab, gen_color)
            gen_loss = loss + l1_loss * penalty
            gen_loss.backward()
            gen_opt.step()

            # Record the losses

            gen_loss_list.append(gen_loss.item())
            disc_loss_list.append(disc_loss.item())


        print(f"Epoch: {epoch+1} , Gen Loss: {gen_loss_list[-1]} , Disc Loss: { disc_loss_list[-1]}")
        
    return gen, disc, gen_opt, disc_opt, gen_loss_list, disc_loss_list