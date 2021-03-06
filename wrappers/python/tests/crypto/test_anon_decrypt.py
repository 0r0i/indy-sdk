from indy import crypto, error

import pytest


@pytest.mark.asyncio
async def test_anon_decrypt_works(wallet_handle, identity_trustee1, message):
    (_, verkey) = identity_trustee1
    encrypted_msg = await crypto.anon_crypt(verkey, message)
    parsed_message = await crypto.anon_decrypt(wallet_handle, verkey, encrypted_msg)
    assert message == parsed_message


@pytest.mark.asyncio
async def test_anon_decrypt_works_for_invalid_anonymous_msg(wallet_handle, identity_trustee1):
    (_, verkey) = identity_trustee1
    msg = "unencrypted message"
    with pytest.raises(error.CommonInvalidStructure):
        await crypto.anon_decrypt(wallet_handle, verkey, msg.encode('utf-8'))


@pytest.mark.asyncio
async def test_parse_msg_msg_works_for_unknown_recipient_vk(wallet_handle, verkey_my1, message):
    encrypted_msg = await crypto.anon_crypt(verkey_my1, message)
    with pytest.raises(error.WalletItemNotFound):
        await crypto.anon_decrypt(wallet_handle, verkey_my1, encrypted_msg)


@pytest.mark.asyncio
async def test_anon_decrypt_works_for_invalid_handle(wallet_handle, identity_trustee1, message):
    (_, verkey) = identity_trustee1
    encrypted_msg = await crypto.anon_crypt(verkey, message)
    with pytest.raises(error.WalletInvalidHandle):
        invalid_wallet_handle = wallet_handle + 1
        await crypto.anon_decrypt(invalid_wallet_handle, verkey, encrypted_msg)
