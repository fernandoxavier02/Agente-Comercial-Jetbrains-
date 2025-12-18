from app.db.session import SessionLocal
from app.models.models import Lead, SourceItem
from datetime import datetime

def test_db_persistence():
    db = SessionLocal()
    try:
        # 1. Criar um item de origem (SourceItem)
        source = SourceItem(
            source="instagram",
            url="http://instagr.am/p/123",
            author_handle="@paciente_teste",
            text="Tenho interesse em tratamento para melasma.",
            timestamp=datetime.now()
        )
        db.add(source)
        db.commit()
        db.refresh(source)
        print(f"SourceItem criado com ID: {source.id}")

        # 2. Criar um Lead associado
        lead = Lead(
            source_item_id=source.id,
            clinic_id=1,
            scores={"lead_score": 85},
            labels={"pain_point": "melasma"},
            status="pending"
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        print(f"Lead criado com ID: {lead.id}")

        # 3. Ler e verificar
        db_lead = db.query(Lead).filter(Lead.id == lead.id).first()
        assert db_lead is not None
        assert db_lead.scores["lead_score"] == 85
        print("Teste de persistência concluído com sucesso!")

    except Exception as e:
        print(f"Erro no teste: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_db_persistence()
